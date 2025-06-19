from datetime import datetime

from pydantic import BaseModel, Field
from ulid import ULID


class CreatePostRequest(BaseModel):
    """게시물 생성 요청 구조"""

    title: str
    content: str


class CreatePostResponse(BaseModel):
    """게시물 저장 응답 구조"""

    id: str


class UpdatePostRequest(BaseModel):
    """게시물 수정 요청 구조"""

    publisher_id: str
    title: str
    content: str


class UpdatePostResponse(BaseModel):
    """게시물 수정 응답 구조"""

    id: str


class CreateCommentRequest(BaseModel):
    """댓글 저장 요청 구조"""

    content: str


class UpdateCommentRequest(BaseModel):
    """댓글 수정 요청 구조"""

    content: str


class CreateCommentResponse(BaseModel):
    """댓글 생성 요청 구조"""

    id: str


class UpdateCommentResponse(BaseModel):
    """댓글 수정 응답 구조"""

    id: str


class GetPostResponse(BaseModel):
    """게시물 조회 응답 구조"""

    id: str
    publisher_name: str
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class GetPostListResponse(BaseModel):
    """게시물 목록 조회 응답 구조"""

    id: str
    publisher_name: str
    title: str
    created_at: datetime


class GetCommentResponse(BaseModel):
    """댓글 조회 응답 구조"""

    id: str
    publisher_name: str
    content: str
    created_at: datetime
    updated_at: datetime


class SavePost(BaseModel):
    """게시물 저장 구조"""

    id: str = str(ULID())
    member_id: str
    title: str
    content: str
    like_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    is_deleted: bool = False


class SaveComment(BaseModel):
    """댓글 저장 구조"""

    id: str = str(ULID())
    member_id: str
    post_id: str
    content: str
    like_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    updated_at: datetime = Field(default_factory=lambda: datetime.now())
    is_deleted: bool = False