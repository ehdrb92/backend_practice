from pydantic import BaseModel

from enums.member_role import MemberRole


class JoinMemberRequest(BaseModel):
    """회원가입 요청 스키마"""

    email: str
    password: str
    address: str
    name: str
    role: MemberRole


class JoinMemberResponse(BaseModel):
    """회원가입 응답 스키마"""

    id: int


class LoginMemberRequest(BaseModel):
    """로그인 요청 스키마"""

    email: str
    password: str


class LoginMemberResponse(BaseModel):
    """로그인 응답 스키마"""

    id: int
    email: str
    address: str
    name: str
    role: MemberRole
