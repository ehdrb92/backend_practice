from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from post.schemas import (
    CreatePostRequest,
    CreatePostResponse,
    GetPostResponse,
    GetPostListResponse,
    GetCommentResponse,
    UpdatePostRequest,
    UpdatePostResponse,
    CreateCommentRequest,
    CreateCommentResponse,
    UpdateCommentRequest,
    UpdateCommentResponse
)
from member.schemas import TokenPayload
from post.service.post import PostService
from database import AsyncSession
from containers import Container
from dependencies import get_current_user, get_session

router = APIRouter(prefix="/api/v1", tags=["posts"])


@router.post(
    "/post", response_model=CreatePostResponse, status_code=status.HTTP_201_CREATED
)
@inject
async def create_post(
    create_post_request: CreatePostRequest,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.create_post(session, create_post_request, current_user.sub)


@router.get(
    "/post/{post_id}", response_model=GetPostResponse, status_code=status.HTTP_200_OK
)
@inject
async def get_post(
    post_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.get_post(session, post_id)


@router.get(
    "/posts", response_model=List[GetPostListResponse], status_code=status.HTTP_200_OK
)
@inject
async def get_posts(
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.get_posts(session)


@router.put(
    "/post/{post_id}", response_model=UpdatePostResponse, status_code=status.HTTP_200_OK
)
@inject
async def update_post(
    post_id: str,
    update_post_request: UpdatePostRequest,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.update_post(session, post_id, update_post_request, current_user.sub)


@router.delete("/post/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_post(
    post_id: str,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.delete_post(session, post_id, current_user.sub)


@router.post("/post/{post_id}/like", status_code=status.HTTP_200_OK)
@inject
async def toggle_post_like(
    post_id: str,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.toggle_post_like(session, current_user.sub, post_id)


@router.post(
    "/post/{post_id}/comment",
    response_model=CreateCommentResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_comment(
    post_id: str,
    save_comment_request: CreateCommentRequest,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.create_comment(session, post_id, current_user.sub, save_comment_request)


@router.get(
    "/post/{post_id}/comments",
    response_model=List[GetCommentResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_comments(
    post_id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.get_comments(session, post_id)


@router.put(
    "/post/{post_id}/comment/{comment_id}",
    response_model=UpdateCommentResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_comment(
    post_id: str,
    comment_id: str,
    update_comment_request: UpdateCommentRequest,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.update_comment(session, post_id, comment_id, current_user.sub, update_comment_request)


@router.delete(
    "/post/{post_id}/comment/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_comment(
    post_id: str,
    comment_id: str,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.delete_comment(session, post_id, comment_id, current_user.sub)


@router.post(
    "/post/{post_id}/comment/{comment_id}/like", status_code=status.HTTP_200_OK
)
@inject
async def toggle_comment_like(
    post_id: str,
    comment_id: str,
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    post_service: PostService = Depends(Provide[Container.post_service]),
):
    return await post_service.toggle_comment_like(session, current_user.sub, comment_id)
