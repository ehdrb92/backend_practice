from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from auth.schemas import TokenPayload
from database import AsyncSession
from dependencies import get_current_user, get_db_session
from comment.service import create, get_all_filter_by_post_id, update, delete
from comment.schemas import (
    GetCommentResponse,
    CreateCommentRequest,
    CreateCommentResponse,
    UpdateCommentRequest,
    UpdateCommentResponse,
)

router = APIRouter(prefix="/v1", tags=["comments"])


@router.post("/comment", response_model=CreateCommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    create_comment_request: CreateCommentRequest,
):
    create_comment_request.publisher_id = current_user.sub
    return await create(db_session, create_comment_request)


@router.get("/post/{id}/comments", response_model=List[GetCommentResponse], status_code=status.HTTP_200_OK)
async def get_post_comments(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    id: str,
):
    return await get_all_filter_by_post_id(db_session, id)


@router.put("/comment/{id}", response_model=UpdateCommentResponse, status_code=status.HTTP_200_OK)
async def update_comment(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    id: str,
    update_comment_request: UpdateCommentRequest,
):
    update_comment_request.publisher_id = current_user.sub
    return await update(db_session, id, update_comment_request)


@router.delete("/comment/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    id: str,
):
    return await delete(db_session, id, current_user.sub)


@router.post("/comment/{id}/like", status_code=status.HTTP_200_OK)
async def toggle_comment_like(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    id: str,
):
    # return await post_service.toggle_comment_like(session, current_user.sub, comment_id)
    pass
