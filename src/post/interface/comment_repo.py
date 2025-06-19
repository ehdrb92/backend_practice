from typing import List
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from post.schemas import SaveComment
from post.models.comment import Comment


class ICommentRepository(ABC):
    @abstractmethod
    async def save(
        self, session: AsyncSession, save_comment: SaveComment
    ) -> Comment:
        pass

    @abstractmethod
    async def find_by_id(self, session: AsyncSession, id: str) -> Comment:
        pass

    @abstractmethod
    async def find_all(
        self, session: AsyncSession, post_id: str, offset: int, limit: int
    ) -> List[Comment]:
        pass

    @abstractmethod
    async def delete(self, session: AsyncSession, id: str) -> None:
        pass

    @abstractmethod
    async def inc_like_count(
        self, session: AsyncSession, member_id: str, comment_id: str
    ) -> None:
        pass

    @abstractmethod
    async def dec_like_count(self, session: AsyncSession, member_id: str, comment_id: str) -> None:
        pass

    @abstractmethod
    async def is_liked(
        self,
        session: AsyncSession,
        member_id: str,
        comment_id: str,
    ) -> bool:
        pass
