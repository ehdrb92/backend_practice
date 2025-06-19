# 백엔드 개발 학습

API 서버 개발, 데이터베이스, 도커, 쿠버네티스 등 백엔드 개발자가 다루는 다양한 기술을 다루어 보기 위한 레포지토리입니다.

## API 서버 개발

- FastAPI
- PostgreSQL
    `$ docker run --name dev-db -p 5432:5432 -e POSTGRES_USER=dev -e POSTGRES_PASSWORD=dev -e POSTGRES_DB=dev -d postgres:14.17`
- Alembic
  - `alembic revision --autogenerate -m "{message}"`
  - `alembic upgrade head`

## 전체 로직 레이어 별 역할

- Controller(Router)
  - API 엔드포인트 정의 및 요청 접수
  - 요청 데이터 유효성 검증
  - HTTP 응답 형식 및 상태 코드 관리
- Service
  - 비즈니스 로직 (비밀번호 해싱, 이메일 중복 확인 등)
  - 트랜잭션 관리
  - 데이터 변환 및 가공
- Repository
  - 데이터베이스 통신
  - RAW SQL 혹은 ORM을 사용한 CRUD
  - 데이터 영속성 처리