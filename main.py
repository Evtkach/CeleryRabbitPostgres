from fastapi import FastAPI
from worker import process_user_report

app = FastAPI(title="FastAPI + Celery Service")


@app.post("/generate-report/{user_id}")
async def trigger_background_report(user_id: int):
    # Отправляем задачу в RabbitMQ фоном (.delay)
    task = process_user_report.delay(user_id)

    # Сразу возвращаем клиенту 202 Accepted и ID задачи
    return {
        "status": "Task dispatched to worker",
        "task_id": task.id
    }
