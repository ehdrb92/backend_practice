from datetime import datetime

from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    """게시물 생성 요청 구조"""

    publisher_id: str | None = None
    title: str
    content: str


class CreatePostResponse(BaseModel):
    """게시물 저장 응답 구조"""

    id: str


class UpdatePostRequest(BaseModel):
    """게시물 수정 요청 구조"""

    publisher_id: str | None = None
    title: str
    content: str


class UpdatePostResponse(BaseModel):
    """게시물 수정 응답 구조"""

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
