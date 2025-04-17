from fastapi import APIRouter, Depends, status
from dependency_injector.wiring import inject, Provide

from member.schemas import JoinMemberRequest, JoinMemberResponse, LoginMemberRequest, LoginMemberResponse
from containers import Container
from member.service import MemberService

router = APIRouter(prefix="/api/v1", tags=["members"])


@router.post("/member/join", response_model=JoinMemberResponse, status_code=status.HTTP_201_CREATED)
@inject
async def join(
    join_member_request: JoinMemberRequest,
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    member = await member_service.join(join_member_request)
    return member


@router.post("/member/login", response_model=LoginMemberResponse, status_code=status.HTTP_200_OK)
@inject
async def login(
    login_member_request: LoginMemberRequest,
    member_service: MemberService = Depends(Provide[Container.member_service]),
):
    member = await member_service.login(login_member_request)
    return member
