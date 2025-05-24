from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from src.utils.auth_handler import AuthHandler
from src.member.schemas import (
    JoinMemberRequest,
    JoinMemberResponse,
    GetMemberResponse,
    UpdateMemberRequest,
)
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
        # 회원 식별자 생성
        member.id = str(uuid4())

        # 비밀번호 해싱
        hashed_password = self.auth_handler.hash_password(member.password)
        member.password = hashed_password

        # 회원 저장
        new_member = await self.member_repository.save(session, member)

        # 세션 커밋 및 새로고침
        await session.commit()
        await session.refresh(new_member)
        return JoinMemberResponse(id=new_member.id)

    async def login(
        self,
        email: str,
        password: str,
        session: AsyncSession,
    ) -> str:
        # 이메일로 회원 조회
        member = await self.member_repository.find_by_email(session, email)

        # 회원 존재 검증
        if not member:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.",
            )

        # 비밀번호 검증
        if not self.auth_handler.check_password(password, member.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.",
            )

        # 토큰 생성 및 발행
        access_token = self.auth_handler.create_access_token(
            payload={"sub": member.id, "role": member.role}
        )
        return access_token

    async def get_member(
        self,
        member_id: str,
        session: AsyncSession,
    ) -> GetMemberResponse:
        # 회원 조회
        member = await self.member_repository.find_by_id(session, member_id)

        # 회원 존재 검증
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="회원을 찾을 수 없습니다.",
            )

        return GetMemberResponse(
            id=member.id,
            email=member.email,
            address=member.address,
            name=member.name,
            role=member.role,
        )

    async def get_members(
        self,
        session: AsyncSession,
    ) -> List[GetMemberResponse]:
        # 모든 회원 조회
        members = await self.member_repository.find_all(session)

        # 회원 목록 반환
        return [
            GetMemberResponse(
                id=member.id,
                email=member.email,
                address=member.address,
                name=member.name,
                role=member.role,
            )
            for member in members
        ]

    async def update_member(
        self,
        member: UpdateMemberRequest,
        session: AsyncSession,
    ) -> GetMemberResponse:
        # 회원 수정
        member = await self.member_repository.update(session, member)

        # 세션 커밋
        await session.commit()

        # 수정된 회원 반환
        return GetMemberResponse(
            id=member.id,
            email=member.email,
            address=member.address,
            name=member.name,
            role=member.role,
        )

    async def delete_member(
        self,
        member_id: str,
        session: AsyncSession,
    ) -> None:
        # 회원 존재 검증
        member = await self.member_repository.find_by_id(session, member_id)
        if not member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="회원을 찾을 수 없습니다.",
            )

        # 회원 삭제
        await self.member_repository.delete(session, member_id)

        # 세션 커밋
        await session.commit()
