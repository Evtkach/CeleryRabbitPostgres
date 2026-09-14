import os
from celery import Celery
from celery.schedules import crontab

# Читаем переменные окружения (подставьте свои доступы)
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672//")
# Для Postgres в качестве backend используем схему db+postgresql
POSTGRES_URL = os.getenv("DATABASE_URL", "db+postgresql://user:password@localhost:5432/dbname")

# Инициализируем Celery
celery_app = Celery(
    "tasks",
    broker=RABBITMQ_URL,
    backend=POSTGRES_URL
)

# Обязательно настраиваем часовой пояс для корректного расписания
celery_app.conf.timezone = "Europe/Moscow"


# --- Описание задач ---

@celery_app.task(name="sync_database_task")
def sync_database_task():
    """Задача, которая будет работать по расписанию."""
    # Здесь логика работы с Postgres
    print("Запуск периодической синхронизации базы данных...")
    return "Синхронизация успешно завершена"


@celery_app.task(name="process_user_report")
def process_user_report(user_id: int):
    """Задача, которая будет триггериться по ручке."""
    print(f"Началась генерация тяжелого отчета для пользователя {user_id}...")
    # Имитация долгой работы
    import time
    time.sleep(10)
    return f"Отчет для {user_id} готов"


# --- Настройка Celery Beat (Расписание) ---

celery_app.conf.beat_schedule = {
    # Имя конфигурации
    "run-sync-every-midnight": {
        "task": "sync_database_task",
        # Запуск каждый день в 00:00 (crontab-формат)
        "schedule": crontab(hour=0, minute=0),
    },
    "run-heartbeat-every-5-minutes": {
        "task": "sync_database_task",
        # Альтернативный вариант: запуск каждые 5 минут (в секундах)
        "schedule": 300.0,
    },
}
