from fastapi import FastAPI
import uvicorn

from routers.member import router as member_router
from containers import Container

app = FastAPI(debug=True, title="Backend Practice", docs_url="/api/docs", redoc_url="/api/redoc")

# IoC 컨테이너 설정
app.container = Container()

# 라우터
app.include_router(member_router)


@app.get("/api/v1/health")
async def health():
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
