from datetime import datetime

from pydantic import BaseModel, EmailStr

from member.enums import MemberRole


class JoinRequest(BaseModel):
    """회원가입 요청 구조"""

    email: EmailStr
    password: str
    address: str
    name: str
    role: MemberRole | None = None


class JoinResponse(BaseModel):
    """회원가입 응답 구조"""

    id: str


class LoginResponse(BaseModel):
    """로그인 응답 구조"""

    token: str


class UpdateMemberRequest(BaseModel):
    """회원정보 수정 요청 구조"""

    email: EmailStr
    address: str
    name: str


class UpdateMemberResponse(BaseModel):
    """회원정보 수정 응답 구조"""

    id: str


class GetMemberResponse(BaseModel):
    """회원정보 조회 응답 구조"""

    id: str
    email: EmailStr
    address: str
    name: str
    role: MemberRole
    created_at: datetime
