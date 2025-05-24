from sqlalchemy import Column, String, Enum

from src.database import Base
from src.member.enums import MemberRole


class Member(Base):
    """
    회원 모델

    id: 회원 식별자
    email: 이메일
    password: 비밀번호
    address: 주소
    name: 이름
    role: 권한
    """

    __tablename__ = "member"

    id = Column(String(36), primary_key=True)  # UUID
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    name = Column(String(30), nullable=False)
    role = Column(Enum(MemberRole), nullable=False)
