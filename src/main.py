from fastapi import FastAPI
import uvicorn

app = FastAPI(debug=True, title="Backend Practice", docs_url="/api/docs", redoc_url="/api/redoc")


@app.get("/api")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000)
