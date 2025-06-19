from datetime import datetime
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from member.interface.member_repo import IMemberRepository
from member.models.member import Member
from member.schemas import SaveMember


class MemberORMRepository(IMemberRepository):
    """
    ORM 방식으로 회원 모델을 관리하는 레포지토리
    """

    async def save(
        self,
        session: AsyncSession,
        save_member: SaveMember,
    ) -> Member:
        try:
            member = Member(
                id=save_member.id,
                email=save_member.email,
                password=save_member.password,
                address=save_member.address,
                name=save_member.name,
                role=save_member.role,
                created_at=save_member.created_at,
                is_deleted=save_member.is_deleted,
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
            query = await session.execute(
                select(Member)
                .where(Member.email == email, Member.is_deleted == False)
            )

            return query.scalar_one_or_none()
        except Exception as e:
            print(f"[MemberRepository.find_by_email] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_by_id(self, session: AsyncSession, id: str) -> Member:
        try:
            query = await session.execute(
                select(Member).where(Member.id == id, Member.is_deleted == False)
            )

            return query.scalar_one_or_none()
        except Exception as e:
            print(f"[MemberRepository.find_by_id] 에러가 발생했습니다: {str(e)}")
            raise e

    async def find_all(self, session: AsyncSession) -> Sequence[Member]:
        try:
            query = await session.execute(
                select(Member).where(Member.is_deleted == False)
            )

            return query.scalars().all()
        except Exception as e:
            print(f"[MemberRepository.find_all] 에러가 발생했습니다: {str(e)}")
            raise e

    async def delete(self, session: AsyncSession, member: Member) -> None:
        try:
            await session.delete(member)
        except Exception as e:
            print(f"[MemberRepository.delete] 에러가 발생했습니다: {str(e)}")
            raise e
