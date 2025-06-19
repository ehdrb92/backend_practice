from typing import Sequence
from datetime import datetime

from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from post.models.comment import Comment
from post.schemas import SaveComment
from post.models.comment_like import CommentLike
from post.interface.comment_repo import ICommentRepository


class CommentORMRepository(ICommentRepository):
    """
    ORM 방식으로 댓글 모델을 관리하는 레포지토리
    """

    async def save(
        self, session: AsyncSession, save_comment: SaveComment
    ) -> Comment:
        try:
            comment = Comment(
                id=save_comment.id,
                member_id=save_comment.member_id,
                post_id=save_comment.post_id,
                content=save_comment.content,
                like_count=save_comment.like_count,
                created_at=save_comment.created_at,
                updated_at=save_comment.updated_at,
                is_deleted=save_comment.is_deleted,
            )
            session.add(comment)
            await session.flush()
            await session.refresh(comment)
            return comment
        except Exception as e:
            print(f"[CommentRepository.save] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_by_id(self, session: AsyncSession, id: str) -> Comment:
        try:
            query = await session.execute(select(Comment).where(Comment.id == id, Comment.is_deleted == False))
            comment = query.scalar_one_or_none()

            return comment
        except Exception as e:
            print(f"[CommentRepository.find_by_id] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_all(
        self, session: AsyncSession, post_id: str, offset: int, limit: int
    ) -> Sequence[Comment]:
        try:
            query = await session.execute(
                select(Comment)
                .where(Comment.post_id == post_id, Comment.is_deleted == False)
                .offset(offset)
                .limit(limit)
            )
            comments = query.scalars().all()
            return comments
        except Exception as e:
            print(f"[CommentRepository.find_all] 에러가 발생했습니다: {str(e)}")
            raise e

    async def delete(self, session: AsyncSession, comment: Comment) -> None:
        try:
            await session.delete(comment)
        except Exception as e:
            print(f"[CommentRepository.delete] 에러가 발생했습니다: {str(e)}")
            raise e

    async def inc_like_count(
        self, session: AsyncSession, member_id: str, comment_id: str
    ) -> None:
        """댓글의 좋아요 수를 증가시키는 메서드"""
        try:
            await session.execute(
                update(Comment)
                .where(Comment.id == comment_id)
                .values(like_count=Comment.like_count + 1, updated_at=datetime.now())
            )

            await session.execute(
                insert(CommentLike).values(
                    comment_id=comment_id,
                    member_id=member_id,
                )
            )
        except Exception as e:
            print(f"[CommentRepository.inc_like_count] 에러가 발생했습니다: {str(e)}")
            raise e

    async def dec_like_count(
        self, session: AsyncSession, member_id: str, comment_id: str
    ) -> None:
        """댓글의 좋아요 수를 감소시키는 메서드"""
        try:
            await session.execute(
                update(Comment)
                .where(Comment.id == comment_id)
                .values(like_count=Comment.like_count - 1, updated_at=datetime.now())
            )

            await session.execute(
                delete(CommentLike).where(
                    CommentLike.comment_id == comment_id,
                    CommentLike.member_id == member_id,
                )
            )
        except Exception as e:
            print(f"[CommentRepository.dec_like_count] 에러가 발생했습니다: {str(e)}")
            raise e

    async def is_liked(
        self,
        session: AsyncSession,
        member_id: str,
        comment_id: str,
    ) -> bool:
        try:
            query = await session.execute(
                select(CommentLike).where(
                    CommentLike.member_id == member_id,
                    CommentLike.comment_id == comment_id,
                )
            )
            return query.scalar_one_or_none() is not None
        except Exception as e:
            print(f"[CommentRepository.is_liked] 에러가 발생했습니다: {str(e)}")
            raise e
