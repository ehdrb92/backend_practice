FROM python:3.13-alpine

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]