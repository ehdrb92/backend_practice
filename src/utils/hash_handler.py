import bcrypt


class HashHandler:
    """비밀번호 해싱 핸들러"""

    def hash_password(self, password: str) -> bytes:
        """
        비밀번호 해싱

        Args:
            password: 해싱할 비밀번호

        Returns:
            bytes: 해싱된 비밀번호
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str, hashed_password: bytes) -> bool:
        """
        비밀번호 검증

        Args:
            password: 검증할 비밀번호
            hashed_password: 해싱된 비밀번호

        Returns:
            bool: 검증 결과
        """
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
