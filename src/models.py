from datetime import datetime

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from member.enums import MemberRole


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
    """

    __tablename__ = "member"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)  # UUID
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    role: Mapped[MemberRole] = mapped_column(nullable=False, default=MemberRole.USER)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    posts: Mapped["Post"] = relationship(back_populates="member", cascade="all, delete")
    comments: Mapped["Comment"] = relationship(back_populates="member", cascade="all, delete")


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
    """

    __tablename__ = "post"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)  # ULID
    member_id: Mapped[str] = mapped_column(String(36), ForeignKey("member.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)

    member: Mapped["Member"] = relationship(back_populates="posts")
    comments: Mapped["Comment"] = relationship(back_populates="post", cascade="all, delete")


class PostLike(Base):
    """
    게시물 좋아요 기록 테이블

    post_id: 좋아요 누른 게시물
    member_id: 좋아요 누른 사용자
    """

    __tablename__ = "post_like"

    post_id: Mapped[str] = mapped_column(String(26), ForeignKey("post.id"), primary_key=True)
    member_id: Mapped[str] = mapped_column(String(26), ForeignKey("member.id"), primary_key=True)


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)  # ULID
    member_id: Mapped[str] = mapped_column(String(36), ForeignKey("member.id"), nullable=False)
    post_id: Mapped[str] = mapped_column(String(26), ForeignKey("post.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    like_count: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(nullable=False)

    member: Mapped["Member"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")


class CommentLike(Base):
    __tablename__ = "comment_like"

    comment_id: Mapped[str] = mapped_column(String(26), ForeignKey("comment.id"), primary_key=True)
    member_id: Mapped[str] = mapped_column(String(26), ForeignKey("member.id"), primary_key=True)
