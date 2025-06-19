from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn

from member.router.member import router as member_router
from post.router.post import router as post_router
from containers import Container
from exception_handler import (
    validation_exception_handler,
    http_exception_handler,
    internal_server_error_handler,
)
from middlewares import get_middleware
from database import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 데이터베이스 테이블 생성
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 데이터베이스 테이블 정리
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(
    debug=True,
    title="Backend Practice",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    middleware=get_middleware(),
    lifespan=lifespan
)

# IoC 컨테이너 설정
container = Container()
container.wire(packages=["member", "post"])

# 라우터
app.include_router(member_router)
app.include_router(post_router)

# 예외 처리 핸들러
app.add_exception_handler(RequestValidationError, validation_exception_handler) # type: ignore
app.add_exception_handler(HTTPException, http_exception_handler) # type: ignore
app.add_exception_handler(Exception, internal_server_error_handler)


@app.get("/api/v1/health")
async def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok"})


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, workers=1)
