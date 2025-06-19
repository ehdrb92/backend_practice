from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field

from member.enums.member_role import MemberRole


class JoinRequest(BaseModel):
    """회원가입 요청 구조"""

    email: EmailStr
    password: str
    address: str
    name: str
    role: MemberRole | None

class JoinResponse(BaseModel):
    """회원가입 응답 구조"""

    id: str


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


class TokenPayload(BaseModel):
    """토큰 페이로드 구조"""

    sub: str
    role: MemberRole
    exp: datetime
    iat: datetime
    jti: str

class SaveMember(BaseModel):
    """회원 저장 구조"""

    id: str = Field(default_factory=lambda: str(uuid4()))
    email: EmailStr
    password: str
    address: str
    name: str
    role: MemberRole = MemberRole.USER
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    is_deleted: bool = False