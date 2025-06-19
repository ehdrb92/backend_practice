from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class CommentLike(Base):
    """
    댓글 좋아요 기록 테이블

    comment_id: 좋아요 누른 댓글
    member_id: 좋아요 누른 사용자
    """

    __tablename__ = "comment_like"

    comment_id: Mapped[str] = mapped_column(String(26), ForeignKey("comment.id"), primary_key=True)
    member_id: Mapped[str] = mapped_column(String(26), ForeignKey("member.id"), primary_key=True)