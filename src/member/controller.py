from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from dependency_injector.wiring import inject, Provide

from src.member.schemas import JoinMemberRequest, JoinMemberResponse, GetMemberResponse
from src.containers import Container
from src.member.service import MemberService

router = APIRouter(prefix="/api/v1", tags=["members"])


@router.post(
    "/member/join",
    response_model=JoinMemberResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def join(
    join_member_request: JoinMemberRequest,
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    return await member_service.join(join_member_request)


@router.post("/member/login", response_model=str, status_code=status.HTTP_200_OK)
@inject
async def login(
    oauth2_request: Annotated[OAuth2PasswordRequestForm, Depends()],
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    access_token = await member_service.login(
        oauth2_request.username, oauth2_request.password
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
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    member = await member_service.get_member(member_id)
    return member
