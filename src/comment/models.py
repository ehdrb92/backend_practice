from datetime import datetime

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)  # ULID
    member_id: Mapped[str] = mapped_column(String(36), ForeignKey("member.id"), nullable=False)
    post_id: Mapped[str] = mapped_column(String(26), ForeignKey("post.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)

    member = relationship("Member", back_populates="comments")
    post = relationship("Post", back_populates="comments")


class CommentLike(Base):
    __tablename__ = "comment_like"

    comment_id: Mapped[str] = mapped_column(String(26), ForeignKey("comment.id"), primary_key=True)
    member_id: Mapped[str] = mapped_column(String(26), ForeignKey("member.id"), primary_key=True)
