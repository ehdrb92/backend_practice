from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn

from src.member.router import router as member_router
from src.containers import Container
from src.exceptions import (
    validation_exception_handler,
    http_exception_handler,
    internal_server_error_handler,
)
from src.middlewares import get_middleware

app = FastAPI(
    debug=True,
    title="Backend Practice",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    middleware=get_middleware(),
)

# IoC 컨테이너 설정
container = Container()
container.wire(packages=["src.member"])
app.container = container

# 라우터
app.include_router(member_router)

# 예외 처리 핸들러
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, internal_server_error_handler)


@app.get("/api/v1/health")
async def health():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "ok"})


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
