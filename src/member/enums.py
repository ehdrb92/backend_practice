from enum import StrEnum


class MemberRole(StrEnum):
    """
    회원 권한

    USER: 일반 사용자
    ADMIN: 관리자
    """

    USER = "USER"
    ADMIN = "ADMIN"
