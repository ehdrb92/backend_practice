from typing import Sequence
from datetime import datetime

from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from post.models.post import Post
from post.schemas import SavePost
from post.interface.post_repo import IPostRepository
from post.models.post_like import PostLike


class PostORMRepository(IPostRepository):
    """
    ORM 방식으로 게시물 모델을 관리하는 레포지토리
    """

    async def save(
        self, session: AsyncSession, save_post: SavePost
    ) -> Post:
        try:
            post = Post(
                id=save_post.id,
                member_id=save_post.member_id,
                title=save_post.title,
                content=save_post.content,
                like_count=save_post.like_count,
                created_at=save_post.created_at,
                updated_at=save_post.updated_at,
                is_deleted=save_post.is_deleted,
            )
            session.add(post)
            await session.flush()
            await session.refresh(post)
            return post
        except Exception as e:
            print(f"[PostRepository.save] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_by_id(self, session: AsyncSession, id: str) -> Post | None:
        try:
            query = await session.execute(select(Post).options(selectinload(Post.member)).filter(Post.id == id).where(Post.is_deleted == False))
            post = query.scalar_one_or_none()

            return post
        except Exception as e:
            print(f"[PostRepository.find_by_id] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_all(
        self, session: AsyncSession, offset: int, limit: int
    ) -> Sequence[Post]:
        try:
            query = await session.execute(
                select(Post)
                .options(selectinload(Post.member))
                .offset(offset)
                .limit(limit)
                .where(Post.is_deleted == False)
            )
            posts = query.scalars().all()
            return posts
        except Exception as e:
            print(f"[PostRepository.find_all] 에러가 발생했습니다: {str(e)}")
            raise e

    async def delete(self, session: AsyncSession, post: Post) -> None:
        try:
            await session.delete(post)
        except Exception as e:
            print(f"[PostRepository.delete] 에러가 발생했습니다: {str(e)}")
            raise e

    async def inc_like_count(
        self,
        session: AsyncSession,
        member_id: str,
        id: str,
    ) -> None:
        """게시물의 좋아요 수를 증가시키는 메서드"""
        try:
            await session.execute(
                update(Post)
                .where(Post.id == id)
                .values(like_count=Post.like_count + 1, updated_at=datetime.now())
            )

            await session.execute(
                insert(PostLike).values(
                    post_id=id,
                    member_id=member_id,
                )
            )
        except Exception as e:
            print(f"[PostRepository.inc_like_count] 에러가 발생했습니다: {str(e)}")
            raise e

    async def dec_like_count(
        self,
        session: AsyncSession,
        member_id: str,
        id: str,
    ) -> None:
        try:
            await session.execute(
                update(Post)
                .where(Post.id == id)
                .values(like_count=Post.like_count - 1, updated_at=datetime.now())
            )

            await session.execute(
                delete(PostLike).where(
                    PostLike.post_id == id,
                    PostLike.member_id == member_id,
                )
            )
        except Exception as e:
            print(f"[PostRepository.dec_like_count] 에러가 발생했습니다: {str(e)}")
            raise e

    async def is_liked(
        self,
        session: AsyncSession,
        member_id: str,
        post_id: str,
    ) -> bool:
        try:
            query = await session.execute(
                select(PostLike).where(
                    PostLike.member_id == member_id,
                    PostLike.post_id == post_id,
                )
            )
            return query.scalar_one_or_none() is not None
        except Exception as e:
            print(f"[PostRepository.is_liked] 에러가 발생했습니다: {str(e)}")
            raise e
