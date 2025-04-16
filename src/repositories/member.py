from sqlalchemy.orm import Session

from models.member import Member
from schemas.member import JoinMemberRequest


class MemberRepository:
    def create_member(self, session: Session, member: JoinMemberRequest):
        member = Member(email=member.email, password=member.password, address=member.address, name=member.name)
        session.add(member)
        return member

    def get_member_by_email(self, session: Session, email: str):
        return session.query(Member).filter(Member.email == email).first()
