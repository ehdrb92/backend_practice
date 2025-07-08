from time import sleep
import random

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


@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def test_job(self):
    try:
        num = random.choice([0, 1, 2])

        sleep(1)

        result = 10 // num

        print(f"result is {result}!")
    except Exception as e:
        print("Exception!!!")
        raise e
