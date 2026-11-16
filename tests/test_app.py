import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from main import app
from worker import process_user_report, sync_database_task, celery_app

client = TestClient(app)


# --- 1. Тесты внутренней логики Celery-задач ---

def test_process_user_report_logic():
    """Проверяет логику генерации отчета без ожидания 10 секунд и без RabbitMQ."""
    # Мокаем стандартный time.sleep, так как он импортируется внутри функции
    with patch("time.sleep") as mock_sleep:
        result = process_user_report.run(user_id=42)

        assert result == "Отчет для 42 готов"
        mock_sleep.assert_called_once_with(10)


def test_sync_database_task_logic():
    """Проверяет выполнение периодической задачи синхронизации."""
    result = sync_database_task.run()
    assert result == "Синхронизация успешно завершена"


def test_celery_task_exception_handling():
    """Проверяет, что задача корректно пробрасывает ошибку при сбое внутри."""
    with patch("time.sleep", side_effect=RuntimeError("Сбой при генерации отчета")):
        with pytest.raises(RuntimeError, match="Сбой при генерации отчета"):
            process_user_report.run(user_id=42)


# --- 2. Тест эндпоинта FastAPI ---

def test_trigger_background_report_endpoint():
    """Проверяет, что API ставит задачу в очередь и возвращает её task_id."""
    # Мокаем метод .delay у задачи прямо в модуле main, где она импортирована
    with patch("main.process_user_report.delay") as mock_delay:
        # Имитируем объект AsyncResult, который возвращает Celery
        mock_task = MagicMock()
        mock_task.id = "test-uuid-1234-5678"
        mock_delay.return_value = mock_task

        response = client.post("/generate-report/42")

        assert response.status_code == 200
        assert response.json() == {
            "status": "Task dispatched to worker",
            "task_id": "test-uuid-1234-5678",
        }
        # Убеждаемся, что задача вызвана с правильным user_id (int)
        mock_delay.assert_called_once_with(42)


# --- 3. Тест конфигурации расписания (Celery Beat) ---

def test_beat_schedule_config():
    """Проверяет наличие и корректность задач в расписании Celery Beat."""
    schedule = celery_app.conf.beat_schedule

    assert "run-sync-every-midnight" in schedule
    assert schedule["run-sync-every-midnight"]["task"] == "sync_database_task"

    assert "run-heartbeat-every-5-minutes" in schedule
    assert schedule["run-heartbeat-every-5-minutes"]["schedule"] == 300.0
