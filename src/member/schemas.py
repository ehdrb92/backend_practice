from pydantic import BaseModel


class JoinMemberRequest(BaseModel):
    email: str
    password: str
    address: str
    name: str


class JoinMemberResponse(BaseModel):
    id: int


class LoginMemberRequest(BaseModel):
    email: str
    password: str


class LoginMemberResponse(BaseModel):
    id: int
    email: str
    address: str
    name: str
