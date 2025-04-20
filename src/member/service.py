from fastapi import HTTPException, status

from member.repository import MemberRepository
from utils.hash_handler import HashHandler
from member.schemas import JoinMemberRequest, JoinMemberResponse, LoginMemberRequest, LoginMemberResponse, GetMemberResponse
from utils.core import to_dict
from database import create_session


class MemberService:
    def __init__(self, member_repository: MemberRepository, hash_handler: HashHandler):
        self.member_repository = member_repository
        self.hash_handler = hash_handler

    async def join(self, member: JoinMemberRequest):
        session = create_session()
        try:
            hashed_password = self.hash_handler.hash_password(member.password)
            member.password = hashed_password
            new_member = self.member_repository.create_member(session, member)
            session.commit()
            session.refresh(new_member)
            return JoinMemberResponse(**to_dict(new_member))
        finally:
            session.close()

    async def login(self, login_member_request: LoginMemberRequest):
        session = create_session()
        try:
            member = self.member_repository.get_member_by_email(session, login_member_request.email)
            if not member:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.")
            if not self.hash_handler.check_password(login_member_request.password, member.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증에 실패했습니다. 이메일 또는 비밀번호를 확인해주세요.")
            return LoginMemberResponse(**to_dict(member))
        finally:
            session.close()

    async def get_member(self, member_id: int):
        session = create_session()
        try:
            member = self.member_repository.get_member_by_id(session, member_id)
            return GetMemberResponse(**to_dict(member))
        finally:
            session.close()
