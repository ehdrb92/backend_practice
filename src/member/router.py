from typing import Annotated, List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from src.member.schemas import (
    JoinMemberRequest,
    JoinMemberResponse,
    GetMemberResponse,
    UpdateMemberRequest,
)
from src.database import AsyncSession
from src.containers import Container
from src.member.service import MemberService
from src.database import get_session

router = APIRouter(prefix="/api/v1", tags=["members"])


@router.post(
    "/member/join",
    response_model=JoinMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def join(
    join_member_request: JoinMemberRequest,
    session: AsyncSession = Depends(get_session),
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    return await member_service.join(join_member_request, session)


@router.post("/member/login", response_model=str, status_code=status.HTTP_200_OK)
@inject
async def login(
    oauth2_request: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    access_token = await member_service.login(
        oauth2_request.username, oauth2_request.password, session
    )
    return JSONResponse(
        content={"access_token": access_token}, status_code=status.HTTP_200_OK
    )


@router.get(
    "/member/{member_id}",
    response_model=GetMemberResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_member(
    member_id: int,
    session: AsyncSession = Depends(get_session),
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    member = await member_service.get_member(member_id, session)
    return member


@router.get(
    "/members",
    response_model=List[GetMemberResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_members(
    session: AsyncSession = Depends(get_session),
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    return await member_service.get_members(session)


@router.patch(
    "/member/{member_id}",
    response_model=GetMemberResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def update_member(
    member_id: int,
    member: UpdateMemberRequest,
    session: AsyncSession = Depends(get_session),
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    member.id = member_id
    return await member_service.update_member(member, session)


@router.delete(
    "/member/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete_member(
    member_id: int,
    session: AsyncSession = Depends(get_session),
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    await member_service.delete_member(member_id, session)
    return
