from datetime import datetime

from pydantic import BaseModel


class CreateCommentRequest(BaseModel):
    """댓글 저장 요청 구조"""

    publisher_id: str | None = None
    post_id: str
    content: str


class UpdateCommentRequest(BaseModel):
    """댓글 수정 요청 구조"""

    publisher_id: str | None = None
    content: str


class CreateCommentResponse(BaseModel):
    """댓글 생성 요청 구조"""

    id: str


class UpdateCommentResponse(BaseModel):
    """댓글 수정 응답 구조"""

    id: str


class GetCommentResponse(BaseModel):
    """댓글 조회 응답 구조"""

    id: str
    publisher_name: str
    content: str
    created_at: datetime
    updated_at: datetime
