from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth_handler import AuthHandler
from src.member.schemas import (
    JoinMemberRequest,
    JoinMemberResponse,
    GetMemberResponse,
    UpdateMemberRequest,
)
from src.utils.core import to_dict
from src.member.irepository import IMemberRepository


class MemberService:
    def __init__(
        self,
        member_repository: IMemberRepository,
        auth_handler: AuthHandler,
    ):
        self.member_repository = member_repository
        self.auth_handler = auth_handler

    async def join(
        self,
        member: JoinMemberRequest,
        session: AsyncSession,
    ) -> JoinMemberResponse:
        hashed_password = self.auth_handler.hash_password(member.password)
        member.password = hashed_password
        new_member = await self.member_repository.save(session, member)
        await session.commit()
        await session.refresh(new_member)
        return JoinMemberResponse(**to_dict(new_member))

    async def login(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ) -> str:
        member = await self.member_repository.find_by_email(session, email)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.",
            )
        if not self.auth_handler.check_password(password, member.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.",
            )
        access_token = self.auth_handler.create_access_token(
            payload={"member_id": member.id, "role": member.role}
        )
        return access_token

    async def get_member(
        self,
        member_id: int,
        session: AsyncSession,
    ) -> GetMemberResponse:
        member = await self.member_repository.find_by_id(session, member_id)
        return GetMemberResponse(**to_dict(member))

    async def get_members(
        self,
        session: AsyncSession,
    ) -> List[GetMemberResponse]:
        members = await self.member_repository.find_all(session)
        return [GetMemberResponse(**to_dict(member)) for member in members]

    async def update_member(
        self,
        member: UpdateMemberRequest,
        session: AsyncSession,
    ) -> GetMemberResponse:
        member = await self.member_repository.update(session, member)
        await session.commit()
        return GetMemberResponse(**to_dict(member))

    async def delete_member(
        self,
        member_id: int,
        session: AsyncSession,
    ) -> None:
        await self.member_repository.delete(session, member_id)
        await session.commit()
