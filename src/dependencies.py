from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Annotated, AsyncGenerator

from src.member.schemas import TokenPayload
from src.config import get_settings
from src.database import AsyncSessionLocal, AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    세션 획득
    """

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    """
    JWT 토큰 검증 및 회원 정보 획득
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="토큰이 유효하지 않습니다.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_payload = TokenPayload(
            sub=payload.get("sub"),
            role=payload.get("role"),
            exp=payload.get("exp"),
            iat=payload.get("iat"),
            jti=payload.get("jti"),
        )
        if token_payload.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return token_payload
