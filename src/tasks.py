from time import sleep

from celery import Celery

from config import get_settings

settings = get_settings()

app = Celery(
    "backgroundapp",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0",
)


@app.task
def send_welcome_email_task():
    print("send_welcome_email_task start!")
    sleep(5)
    print("task success!")
