import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
import uvicorn

from auth.router import router as auth_router
from member.router import router as member_router
from post.router import router as post_router
from comment.router import router as comment_router
from middlewares import get_middleware
from database import engine, Base
from exception_handler import (
    validation_exception_handler,
    http_exception_handler,
    internal_server_error_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


app = FastAPI(
    debug=True,
    title="Backend Practice",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    middleware=get_middleware(),
    lifespan=lifespan,
)

# 라우터
app.include_router(auth_router)
app.include_router(member_router)
app.include_router(post_router)
app.include_router(comment_router)

# 예외 처리 핸들러
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
app.add_exception_handler(Exception, internal_server_error_handler)


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, workers=1)
