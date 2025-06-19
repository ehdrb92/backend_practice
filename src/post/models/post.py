from datetime import datetime

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Post(Base):
    """
    게시물 모델

    id: 게시물 식별자
    member_id: 회원 식별자
    title: 게시물 제목
    content: 게시물 내용
    like_count: 좋아요 수
    created_at: 생성일시
    updated_at: 수정일시
    is_deleted: 논리적 삭제 여부
    """

    __tablename__ = "post"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)  # ULID
    member_id: Mapped[str] = mapped_column(String(36), ForeignKey("member.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False)  # 논리적 삭제 여부

    member = relationship("Member", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
