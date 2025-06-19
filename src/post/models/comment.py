from datetime import datetime

from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Comment(Base):
    """
    댓글 모델

    id: 댓글 식별자
    member_id: 회원 식별자
    post_id: 게시물 식별자
    content: 댓글 내용
    like_count: 좋아요 수
    created_at: 생성일시
    updated_at: 수정일시
    is_deleted: 논리적 삭제 여부
    """

    __tablename__ = "comment"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)  # ULID
    member_id: Mapped[str] = mapped_column(String(36), ForeignKey("member.id"), nullable=False)
    post_id: Mapped[str] = mapped_column(String(26), ForeignKey("post.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)
    is_deleted: Mapped[bool] = mapped_column(nullable=False)  # 논리적 삭제 여부

    member = relationship("Member", back_populates="comments")
    post = relationship("Post", back_populates="comments")
