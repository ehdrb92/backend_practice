from typing import Sequence

from fastapi.middleware import Middleware


def get_middleware() -> Sequence[Middleware]:
    """
    미들웨어 목록 반환
    """
    return []
