from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from member.schemas import SaveMember
from member.models.member import Member


class IMemberRepository(ABC):
    @abstractmethod
    async def save(
        self,
        session: AsyncSession,
        save_member: SaveMember,
    ) -> Member:
        pass

    @abstractmethod
    async def find_by_email(self, session: AsyncSession, email: str) -> Member:
        pass

    @abstractmethod
    async def find_by_id(self, session: AsyncSession, id: str) -> Member:
        pass

    @abstractmethod
    async def find_all(self, session: AsyncSession) -> List[Member]:
        pass

    @abstractmethod
    async def delete(self, session: AsyncSession, member: Member) -> None:
        pass
