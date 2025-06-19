from typing import List
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from post.schemas import SavePost
from post.models.post import Post


class IPostRepository(ABC):
    @abstractmethod
    async def save(
        self, session: AsyncSession, save_post: SavePost
    ) -> Post:
        pass

    @abstractmethod
    async def find_by_id(self, session: AsyncSession, id: str) -> Post:
        pass

    @abstractmethod
    async def find_all(
        self, session: AsyncSession, offset: int, limit: int
    ) -> List[Post]:
        pass

    @abstractmethod
    async def delete(self, session: AsyncSession, post: Post) -> None:
        pass

    @abstractmethod
    async def inc_like_count(
        self, session: AsyncSession, member_id: str, post_id: str
    ) -> None:
        pass

    @abstractmethod
    async def dec_like_count(
        self, session: AsyncSession, member_id: str, post_id: str
    ) -> None:
        pass

    @abstractmethod
    async def is_liked(
        self,
        session: AsyncSession,
        member_id: str,
        post_id: str,
    ) -> bool:
        pass
