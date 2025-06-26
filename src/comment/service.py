from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult
from ulid import ULID

from comment.schemas import CreateCommentRequest, UpdateCommentRequest
from models import Comment, CommentLike


async def create(db_session: AsyncSession, create_comment_request: CreateCommentRequest) -> Comment:
    comment = Comment(
        id=str(ULID()),
        member_id=create_comment_request.publisher_id,
        post_id=create_comment_request.post_id,
        content=create_comment_request.content,
        like_count=0,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db_session.add(comment)
    await db_session.flush()
    await db_session.refresh(comment)
    return comment


async def get_all_filter_by_post_id(db_session: AsyncSession, post_id: str) -> ScalarResult[Comment]:
    return await db_session.scalars(select(Comment).where(Comment.post_id == post_id))


async def update(db_session: AsyncSession, id: str, update_comment_request: UpdateCommentRequest) -> Comment:
    _comment = await db_session.scalar(select(Comment).where(Comment.id == id))

    if not _comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"message": "댓글을 찾을 수 없습니다."}])

    if _comment.member_id != update_comment_request.publisher_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=[{"message": "댓글에 대한 권한이 없습니다."}])

    for field, value in update_comment_request.model_dump(exclude_unset=True).items():
        setattr(_comment, field, value)

    await db_session.commit()
    await db_session.refresh(_comment)

    return _comment


async def update_comment_like(db_session: AsyncSession, id: str, clicker_id: str):
    _comment = await db_session.scalar(select(Comment).where(Comment.id == id))

    if not _comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"message": "댓글을 찾을 수 없습니다."}])

    _comment_like = await db_session.scalar(
        select(CommentLike).where(CommentLike.member_id == clicker_id, CommentLike.comment_id == id)
    )

    if _comment_like:
        await db_session.delete(_comment_like)
        _comment.like_count -= 1
    else:
        comment_like = CommentLike(comment_id=id, member_id=clicker_id)
        db_session.add(comment_like)
        _comment.like_count += 1

    await db_session.commit()


async def delete(db_session: AsyncSession, id: str, publisher_id: str):
    _comment = await db_session.scalar(select(Comment).where(Comment.id == id))

    if not _comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=[{"message": "댓글을 찾을 수 없습니다."}])

    if _comment.member_id != publisher_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=[{"message": "댓글에 대한 권한이 없습니다."}])

    await db_session.delete(_comment)
