from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import ScalarResult

from auth.service import hash_password
from tasks import send_welcome_email_task
from member.models import Member
from member.schemas import JoinRequest, UpdateMemberRequest


async def create(db_session: AsyncSession, join_request: JoinRequest) -> str:
    _member = await db_session.scalar(select(Member).where(Member.email == join_request.email))

    if _member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[{"message": "이미 존재하는 이메일입니다."}],
        )

    hashed_password = hash_password(join_request.password)

    member = Member(
        id=str(uuid4()),
        email=join_request.email,
        password=hashed_password,
        address=join_request.address,
        name=join_request.name,
        created_at=datetime.now(),
    )

    if join_request.role:
        member.role = join_request.role

    db_session.add(member)
    await db_session.flush()
    await db_session.refresh(member)

    send_welcome_email_task.delay()

    return member


async def get(db_session: AsyncSession, id: str) -> Member:
    _member = await db_session.scalar(select(Member).where(Member.id == id))

    if not _member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"message": "회원을 찾을 수 없습니다."}],
        )

    return _member


async def get_all(db_session: AsyncSession) -> ScalarResult[Member]:
    return await db_session.scalars(select(Member))


async def update(db_session: AsyncSession, id: str, update_member_request: UpdateMemberRequest) -> Member:
    _member = await db_session.scalar(select(Member).where(Member.id == id))

    if not _member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"message": "회원을 찾을 수 없습니다."}],
        )

    for field, value in update_member_request.model_dump(exclude_unset=True).items():
        setattr(_member, field, value)

    await db_session.commit()
    await db_session.refresh(_member)

    return _member


async def delete(db_session: AsyncSession, id: str) -> None:
    _member = await db_session.scalar(select(Member).where(Member.id == id))

    if not _member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"message": "회원을 찾을 수 없습니다."}],
        )

    await db_session.delete(_member)
