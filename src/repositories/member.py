from sqlmodel import Session
import bcrypt

from models.member import Member
from schemas.member import CreateMemberRequest


class MemberRepository:
    def create_member(self, session: Session, member: CreateMemberRequest):
        hashed_password = bcrypt.hashpw(member.password.encode("utf-8"), bcrypt.gensalt())

        member = Member(email=member.email, password=hashed_password, address=member.address, name=member.name)
        session.add(member)
        return member
