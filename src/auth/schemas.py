from datetime import datetime

from pydantic import BaseModel

from member.enums import MemberRole


class TokenPayload(BaseModel):
    """토큰 페이로드 구조"""

    sub: str
    role: MemberRole
    exp: datetime
    iat: datetime
    jti: str
