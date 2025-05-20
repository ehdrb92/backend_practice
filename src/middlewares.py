from fastapi import Request, Response, FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
from src.utils.auth_handler import AuthHandler
from jose import JWTError


class JWTValidateMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.auth_handler = AuthHandler()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:

        # 공개 경로 처리
        if request.url.path in ["/api/v1/member/join", "/api/v1/member/login", "/docs"]:
            return await call_next(request)

        # 헤더에서 토큰 추출 및 기본 검증
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = self.auth_handler.decode_access_token(token)
                request.state.token_payload = payload
            except JWTError:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "토큰이 유효하지 않습니다."},
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "토큰이 없습니다."},
            )

        return await call_next(request)


def get_middleware() -> list[BaseHTTPMiddleware]:
    jwt_validate_middleware = Middleware(
        JWTValidateMiddleware,
    )
    return [jwt_validate_middleware]
