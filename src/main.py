from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uvicorn

from auth.router import router as auth_router
from member.router import router as member_router
from post.router import router as post_router
from comment.router import router as comment_router
from middlewares import get_middleware
from exception_handler import (
    validation_exception_handler,
    http_exception_handler,
)


app = FastAPI(
    debug=True,
    title="Backend Practice",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    middleware=get_middleware(),
    lifespan=None,
)


@app.middleware("http")
async def unknown_exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception:
        import traceback

        traceback.print_exc()
        return JSONResponse(
            content={"detail": [{"message": "서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."}]},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return response


# 라우터
app.include_router(auth_router)
app.include_router(member_router)
app.include_router(post_router)
app.include_router(comment_router)

# 예외 처리 핸들러
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000, workers=1)
