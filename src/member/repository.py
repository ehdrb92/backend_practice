from sqlalchemy.orm import Session

from member.model import Member
from member.schemas import JoinMemberRequest


class MemberRepository:
    def create_member(self, session: Session, member: JoinMemberRequest):
        member = Member(email=member.email, password=member.password, address=member.address, name=member.name, role=member.role)
        session.add(member)
        return member

    def get_member_by_email(self, session: Session, email: str):
        return session.query(Member).filter(Member.email == email).first()
