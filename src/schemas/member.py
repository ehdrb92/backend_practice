from pydantic import BaseModel


class CreateMemberRequest(BaseModel):
    email: str
    password: str
    address: str
    name: str


class CreateMemberResponse(BaseModel):
    id: int
