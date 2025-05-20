from typing import List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.member.models import Member
from src.member.schemas import JoinMemberRequest, UpdateMemberRequest
from src.member.irepository import IMemberRepository


class MemberRepository(IMemberRepository):
    async def save(self, session: AsyncSession, member: JoinMemberRequest) -> Member:
        try:
            member = Member(
                email=member.email,
                password=member.password,
                address=member.address,
                name=member.name,
                role=member.role,
            )
            session.add(member)
            await session.flush()
            await session.refresh(member)
            return member
        except Exception as e:
            print(f"[MemberRepository.save] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_by_email(self, session: AsyncSession, email: str) -> Member:
        try:
            query = await session.execute(select(Member).filter(Member.email == email))
            return query.scalar_one_or_none()
        except Exception as e:
            print(f"[MemberRepository.find_by_email] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_by_id(self, session: AsyncSession, member_id: int) -> Member:
        try:
            query = await session.execute(select(Member).filter(Member.id == member_id))
            return query.scalar_one_or_none()
        except Exception as e:
            print(f"[MemberRepository.find_by_id] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_all(self, session: AsyncSession) -> List[Member]:
        try:
            query = await session.execute(select(Member))
            return query.scalars().all()
        except Exception as e:
            print(f"[MemberRepository.find_all] 에러가 발생했습니다: {str(e)}")
            raise e

    async def update(
        self, session: AsyncSession, member: UpdateMemberRequest
    ) -> Member:
        try:
            await session.execute(
                update(Member)
                .filter(Member.id == member.id)
                .values(member.model_dump())
            )
            return member
        except Exception as e:
            print(f"[MemberRepository.update] 에러가 발생했습니다: {str(e)}")
            raise e

    async def delete(self, session: AsyncSession, member_id: int) -> None:
        try:
            await session.execute(delete(Member).filter(Member.id == member_id))
        except Exception as e:
            print(f"[MemberRepository.delete] 에러가 발생했습니다: {str(e)}")
            raise e
