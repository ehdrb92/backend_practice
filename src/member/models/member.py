from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from member.enums.member_role import MemberRole


class Member(Base):
    """
    회원 모델

    id: 회원 식별자
    email: 이메일
    password: 비밀번호
    address: 주소
    name: 이름
    role: 권한
    created_at: 생성일시
    is_deleted: 논리적 삭제 여부
    """

    __tablename__ = "member"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    role: Mapped[MemberRole] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False)  # 논리적 삭제 여부

    posts = relationship("Post", back_populates="member", cascade="all, delete")
    comments = relationship("Comment", back_populates="member", cascade="all, delete")
