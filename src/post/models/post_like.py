from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class PostLike(Base):
    """
    게시물 좋아요 기록 테이블

    post_id: 좋아요 누른 게시물
    member_id: 좋아요 누른 사용자
    """

    __tablename__ = "post_like"

    post_id: Mapped[str] = mapped_column(String(26), ForeignKey("post.id"), primary_key=True)
    member_id: Mapped[str] = mapped_column(String(26), ForeignKey("member.id"), primary_key=True)