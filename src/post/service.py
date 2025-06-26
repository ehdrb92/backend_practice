from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from ulid import ULID

from post.schemas import CreatePostRequest, UpdatePostRequest
from post.models import Post, PostLike


async def create(db_session: AsyncSession, create_post_request: CreatePostRequest):
    post = Post(
        id=str(ULID()),
        member_id=create_post_request.publisher_id,
        title=create_post_request.title,
        content=create_post_request.content,
        like_count=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db_session.add(post)
    await db_session.flush()
    await db_session.refresh(post)
    return post


async def get(db_session: AsyncSession, id: str):
    _post = await db_session.scalar(select(Post).where(Post.id == id))

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"message": "게시물을 찾을 수 없습니다."}])

    return _post


async def get_all(db_session: AsyncSession) -> ScalarResult[Post]:
    return await db_session.scalars(select(Post))


async def update(db_session: AsyncSession, id: str, update_post_request: UpdatePostRequest) -> Post:
    _post = await db_session.scalar(select(Post).where(Post.id == id))

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"message": "게시물을 찾을 수 없습니다."}])

    if _post.member_id != update_post_request.publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=[{"message": "게시물에 대한 권한이 없습니다."}]
        )

    for field, value in update_post_request.model_dump(exclude_unset=True).items():
        setattr(_post, field, value)

    await db_session.commit()
    await db_session.refresh(_post)

    return _post


async def update_post_like(db_session: AsyncSession, id: str, clicker_id: str) -> None:
    _post = await db_session.scalar(select(Post).where(Post.id == id))

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"message": "게시물을 찾을 수 없습니다."}])

    _post_like = await db_session.scalar(
        select(PostLike).where(PostLike.member_id == clicker_id, PostLike.post_id == id)
    )

    if _post_like:
        await db_session.delete(_post_like)
        _post.like_count -= 1
    else:
        post_like = PostLike(post_id=id, member_id=clicker_id)
        db_session.add(post_like)
        _post.like_count += 1

    await db_session.commit()


async def delete(db_session: AsyncSession, id: str, publisher_id: str) -> None:
    _post = await db_session.scalar(select(Post).where(Post.id == id))

    if not _post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"message": "게시물을 찾을 수 없습니다."}])

    if _post.member_id != publisher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=[{"message": "게시물에 대한 권한이 없습니다."}]
        )

    await db_session.delete(_post)
