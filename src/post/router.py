from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from auth.schemas import TokenPayload
from database import AsyncSession
from dependencies import get_current_user, get_db_session
from post.service import create, get, get_all, update, delete, update_post_like
from post.schemas import (
    CreatePostRequest,
    CreatePostResponse,
    GetPostResponse,
    GetPostListResponse,
    UpdatePostRequest,
    UpdatePostResponse,
)

router = APIRouter(prefix="/v1", tags=["posts"])


@router.post("/post", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    create_post_request: CreatePostRequest,
):
    create_post_request.publisher_id = current_user.sub
    return await create(db_session, create_post_request)


@router.get("/post/{id}", response_model=GetPostResponse, status_code=status.HTTP_200_OK)
async def get_post(db_session: Annotated[AsyncSession, Depends(get_db_session)], id: str):
    return await get(db_session, id)


@router.get("/posts", response_model=List[GetPostListResponse], status_code=status.HTTP_200_OK)
async def get_posts(db_session: Annotated[AsyncSession, Depends(get_db_session)]):
    return await get_all(db_session)


@router.put("/post/{id}", response_model=UpdatePostResponse, status_code=status.HTTP_200_OK)
async def update_post(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    id: str,
    update_post_request: UpdatePostRequest,
):
    update_post_request.publisher_id = current_user.sub
    return await update(db_session, id, update_post_request)


@router.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    id: str,
):
    return await delete(db_session, id, current_user.sub)


@router.post("/post/{id}/like", status_code=status.HTTP_200_OK)
async def click_post_like(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    id: str,
):
    return await update_post_like(db_session, id, current_user.sub)
