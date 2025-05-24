from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.member.enums import MemberRole


class JoinMemberRequest(BaseModel):
    """회원가입 요청 스키마"""

    id: str | None = None
    email: EmailStr
    password: str
    address: str
    name: str
    role: MemberRole


class JoinMemberResponse(BaseModel):
    """회원가입 응답 스키마"""

    id: str


class GetMemberResponse(BaseModel):
    """회원 조회 응답 스키마"""

    id: str
    email: EmailStr
    address: str
    name: str
    role: MemberRole


class UpdateMemberRequest(BaseModel):
    """회원 수정 요청 스키마"""

    id: str | None = None
    email: EmailStr
    address: str
    name: str
    role: MemberRole


class TokenPayload(BaseModel):
    """토큰 페이로드"""

    sub: str
    role: MemberRole
    exp: datetime
    iat: datetime
    jti: str
