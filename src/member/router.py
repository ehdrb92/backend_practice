from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status


from database import AsyncSession
from dependencies import get_current_user, get_db_session
from auth.schemas import TokenPayload
from member.enums import MemberRole
from member.service import create, get, get_all, update, delete
from member.schemas import (
    JoinRequest,
    JoinResponse,
    GetMemberResponse,
    UpdateMemberRequest,
    UpdateMemberResponse,
)

router = APIRouter(prefix="/v1", tags=["member"])


@router.post("/join", response_model=JoinResponse, status_code=status.HTTP_201_CREATED)
async def join(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    join_request: JoinRequest,
):
    return await create(db_session, join_request)


@router.get("/member", response_model=GetMemberResponse, status_code=status.HTTP_200_OK)
async def get_member(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
):
    return await get(db_session, current_user.sub)


@router.get(
    "/members",
    response_model=List[GetMemberResponse],
    status_code=status.HTTP_200_OK,
)
async def get_members(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
):
    print(current_user.role)
    print(MemberRole.ADMIN)
    if current_user.role != MemberRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=[{"message": "권한이 없습니다."}],
        )

    return await get_all(db_session)


@router.patch(
    "/member",
    response_model=UpdateMemberResponse,
    status_code=status.HTTP_200_OK,
)
async def update_member(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
    update_member_request: UpdateMemberRequest,
):
    return await update(db_session, current_user.sub, update_member_request)


@router.delete(
    "/member",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_member(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
    current_user: Annotated[TokenPayload, Depends(get_current_user)],
):
    await delete(db_session, current_user.sub)
