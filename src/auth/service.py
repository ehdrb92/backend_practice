from datetime import datetime, timedelta
from uuid import uuid4
from passlib.context import CryptContext

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from models import Member
from config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    비밀번호 해싱

    Args:
        password: 해싱할 비밀번호

    Returns:
        str: 해싱된 비밀번호
    """
    return pwd_context.hash(password)


def check_password(password: str, hashed_password: str) -> bool:
    """
    비밀번호 검증

    Args:
        password: 검증할 비밀번호
        hashed_password: 해싱된 비밀번호

    Returns:
        bool: 검증 결과
    """
    return pwd_context.verify(password, hashed_password)


def create_access_token(payload: dict, expires_delta: timedelta = timedelta(hours=6)):
    """
    액세스 토큰 생성

    엑세스 토큰의 페이로드 구성

    {
        "sub": 사용자 ID,
        "role": 사용자 역할,
        "exp": 토큰 만료 시간,
        "iat": 토큰 발행 시간,
        "jti": 토큰 고유 식별자,
    }

    Args:
        payload: 토큰에 포함할 데이터
        expires_delta: 토큰 만료 시간

    Returns:
        str: 생성된 액세스 토큰
    """
    expire = datetime.now() + expires_delta
    payload.update(
        {
            "exp": expire,
            "iat": datetime.now(),
            "jti": str(uuid4()),
        }
    )
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    액세스 토큰 검증

    Args:
        token: 검증할 액세스 토큰

    Returns:
        dict: 토큰에 포함된 데이터
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        raise e


async def authenticate(db_session: AsyncSession, email: str, password: str) -> str:
    _member = await db_session.scalar(select(Member).where(Member.email == email))

    if not _member:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"message": "인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요."}],
        )

    if not check_password(password, _member.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=[{"message": "인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요."}],
        )

    return create_access_token(payload={"sub": _member.id, "role": _member.role})
