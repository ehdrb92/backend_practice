from pydantic import BaseModel

from src.member.enums import MemberRole


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


class GetMemberResponse(BaseModel):
    """회원 조회 응답 스키마"""

    id: int
    email: str
    address: str
    name: str
    role: MemberRole


class UpdateMemberRequest(BaseModel):
    """회원 수정 요청 스키마"""

    id: int | None = None
    email: str
    address: str
    name: str
    role: MemberRole
