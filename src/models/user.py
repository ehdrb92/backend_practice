from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=False, primary_key=True)
    email: str = Field(default=None, unique=True, index=True)
    password: bytes = Field(default=None, nullable=False)
    address: str = Field(default=None, nullable=False)
    name: str = Field(default=None, nullable=False)
