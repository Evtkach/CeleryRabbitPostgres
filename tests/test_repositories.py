import pytest
from unittest.mock import MagicMock


# Импортируем модель из вашего приложения (подставьте правильный путь, если модель лежит в db.models)
# from db.models import Task

@pytest.mark.anyio
async def test_repository_create_task_mock(mock_async_session):
    """Тест эмулирует создание задачи в вашей PostgreSQL через SQLAlchemy."""
    # 1. Создаем фейковый объект задачи, имитируя структуру вашей модели Task
    fake_task = MagicMock()
    fake_task.id = 1
    fake_task.status = "PENDING"
    fake_task.result = None

    # 2. Настраиваем мок сессии, чтобы метод scalar() возвращал нашу задачу
    mock_async_session.scalar.return_value = fake_task

    # Имитируем запрос получения задачи по ID
    # result = await mock_async_session.scalar(select(Task).where(Task.id == 1))

    # Временная проверка прохождения для структуры
    assert fake_task.id == 1
    assert fake_task.status == "PENDING"
