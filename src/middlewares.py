from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


def get_middleware() -> list[BaseHTTPMiddleware]:
    """
    미들웨어 목록 반환
    """
    return []
