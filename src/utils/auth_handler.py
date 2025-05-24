from datetime import datetime, timedelta
import uuid
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.config import get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthHandler:
    """인증 핸들러"""

    def __init__(self):
        self.settings = get_settings()

    def hash_password(self, password: str) -> str:
        """
        비밀번호 해싱

        Args:
            password: 해싱할 비밀번호

        Returns:
            str: 해싱된 비밀번호
        """
        return pwd_context.hash(password)

    def check_password(self, password: str, hashed_password: str) -> bool:
        """
        비밀번호 검증

        Args:
            password: 검증할 비밀번호
            hashed_password: 해싱된 비밀번호

        Returns:
            bool: 검증 결과
        """
        return pwd_context.verify(password, hashed_password)

    def create_access_token(
        self, payload: dict, expires_delta: timedelta = timedelta(hours=6)
    ):
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
                "jti": str(uuid.uuid4()),
            }
        )
        encoded_jwt = jwt.encode(
            payload, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM
        )
        return encoded_jwt

    def decode_access_token(self, token: str) -> dict:
        """
        액세스 토큰 검증

        Args:
            token: 검증할 액세스 토큰

        Returns:
            dict: 토큰에 포함된 데이터
        """
        try:
            payload = jwt.decode(
                token, self.settings.SECRET_KEY, algorithms=[self.settings.ALGORITHM]
            )
            return payload
        except JWTError as e:
            raise e
