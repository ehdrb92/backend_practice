from typing import List

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth_handler import AuthHandler
from member.schemas import (
    JoinRequest,
    JoinResponse,
    GetMemberResponse,
    UpdateMemberRequest,
    UpdateMemberResponse,
    SaveMember,
)
from member.interface.member_repo import IMemberRepository


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
        session: AsyncSession,
        join_request: JoinRequest,
    ) -> JoinResponse:
        # 이메일 중복 검증
        _member = await self.member_repository.find_by_email(
            session, join_request.email
        )
        if _member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 존재하는 이메일입니다.",
            )

        # 비밀번호 해싱
        hashed_password = self.auth_handler.hash_password(
            join_request.password
        )

        # 회원 저장 요청 객체 생성
        save_member = SaveMember(
            email=join_request.email,
            password=hashed_password,
            address=join_request.address,
            name=join_request.name
        )

        if join_request.role:
            save_member.role = join_request.role

        # 회원 저장
        member = await self.member_repository.save(session, save_member)

        return JoinResponse(id=member.id)

    async def login(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> str:
        # 이메일로 회원 조회
        _member = await self.member_repository.find_by_email(session, email)

        # 회원 존재 검증
        if not _member:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.",
            )

        # 비밀번호 검증
        if not self.auth_handler.check_password(password, _member.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.",
            )

        # 토큰 생성 및 발행
        access_token = self.auth_handler.create_access_token(
            payload={"sub": _member.id, "role": _member.role}
        )
        return access_token

    async def get_member(
        self,
        session: AsyncSession,
        member_id: str,
    ) -> GetMemberResponse:
        # 회원 조회
        _member = await self.member_repository.find_by_id(session, member_id)

        # 회원 존재 검증
        if not _member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="회원을 찾을 수 없습니다.",
            )

        return GetMemberResponse(
            id=_member.id,
            email=_member.email,
            address=_member.address,
            name=_member.name,
            role=_member.role,
            created_at=_member.created_at,
        )

    async def get_members(
        self,
        session: AsyncSession,
    ) -> List[GetMemberResponse]:
        # 모든 회원 조회
        members = await self.member_repository.find_all(session)

        # 회원 목록 반환
        return [GetMemberResponse(
            id=member.id,
            email=member.email,
            address=member.address,
            name=member.name,
            role=member.role,
            created_at=member.created_at,
        ) for member in members]

    async def update_member(
        self,
        session: AsyncSession,
        member_id: str,
        update_member_request: UpdateMemberRequest,
    ) -> UpdateMemberResponse:
        # 회원 존재 검증
        _member = await self.member_repository.find_by_id(session, member_id)

        if not _member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="회원을 찾을 수 없습니다.",
            )

        save_member_request = SaveMember(
            id=member_id,
            email=update_member_request.email,
            password=_member.password,
            address=update_member_request.address,
            name=update_member_request.name,
            role=_member.role,
            created_at=_member.created_at,
        )

        # 회원 수정
        member = await self.member_repository.save(session, save_member_request)

        # 수정된 회원 반환
        return UpdateMemberResponse(id=member.id)

    async def delete_member(
        self,
        session: AsyncSession,
        member_id: str,
    ) -> None:
        # 회원 존재 검증
        _member = await self.member_repository.find_by_id(session, member_id)

        if not _member:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="회원을 찾을 수 없습니다.",
            )

        save_member = SaveMember(
            id=_member.id,
            email=_member.email,
            password=_member.password,
            address=_member.address,
            name=_member.name,
            role=_member.role,
            created_at=_member.created_at,
            is_deleted=False
        )

        await self.member_repository.save(session, save_member)