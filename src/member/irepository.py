from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.member.schemas import JoinMemberRequest, UpdateMemberRequest
from src.member.models import Member


class IMemberRepository(ABC):
    @abstractmethod
    async def save(self, session: AsyncSession, member: JoinMemberRequest) -> Member:
        pass

    @abstractmethod
    async def find_by_email(self, session: AsyncSession, email: str) -> Member:
        pass

    @abstractmethod
    async def find_by_id(self, session: AsyncSession, id: int) -> Member:
        pass

    @abstractmethod
    async def find_all(self, session: AsyncSession) -> List[Member]:
        pass

    @abstractmethod
    async def update(self, session: AsyncSession, member: UpdateMemberRequest):
        pass

    @abstractmethod
    async def delete(self, session: AsyncSession, id: int) -> None:
        pass
