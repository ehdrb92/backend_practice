from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Annotated, AsyncGenerator

from auth.schemas import TokenPayload
from config import get_settings
from database import AsyncSessionLocal, AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = get_settings()


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
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
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_payload = TokenPayload(
            sub=payload.get("sub"),  # type: ignore
            role=payload.get("role"),  # type: ignore
            exp=payload.get("exp"),  # type: ignore
            iat=payload.get("iat"),  # type: ignore
            jti=payload.get("jti"),  # type: ignore
        )
        if token_payload.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return token_payload
