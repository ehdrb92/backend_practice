from sqlalchemy import Column, Integer, String, LargeBinary

from database import Base


class Member(Base):
    __tablename__ = "member"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(LargeBinary, nullable=False)
    address = Column(String(255), nullable=False)
    name = Column(String(30), nullable=False)
