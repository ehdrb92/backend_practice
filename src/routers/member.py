from fastapi import APIRouter, Depends
from sqlmodel import Session

from database import get_session
from repositories.member import MemberRepository
from schemas.member import CreateMemberRequest, CreateMemberResponse
from utils.core import to_dict

router = APIRouter(prefix="/api/v1", tags=["members"])


@router.post("/member", response_model=CreateMemberResponse)
async def create_member(create_member_request: CreateMemberRequest, session: Session = Depends(get_session)):
    member_repository = MemberRepository()
    new_member = member_repository.create_member(session, create_member_request)
    session.commit()
    session.refresh(new_member)
    return CreateMemberResponse(**to_dict(new_member))
