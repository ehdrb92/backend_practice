# 백엔드 개발 학습

API 서버 개발, 데이터베이스, 도커, 쿠버네티스 등 백엔드 개발자가 다루는 다양한 기술을 다루어 보기 위한 레포지토리입니다.

## API 서버 개발

- FastAPI
- PostgreSQL
    `$ docker run --name dev-db -p 5432:5432 -e POSTGRES_USER=dev -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=dev -d postgres`
- Alembic
  - `alembic revision --autogenerate -m "{message}"`
  - `alembic upgrade head`