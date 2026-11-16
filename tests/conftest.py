import sys
from pathlib import Path
import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

# Добавляем корневую папку проекта в пути поиска модулей Python
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def mock_async_session(mocker):
    """Фикстура для полной подмены асинхронной сессии SQLAlchemy."""
    session = mocker.MagicMock(spec=AsyncSession)
    session.execute = mocker.AsyncMock()
    session.commit = mocker.AsyncMock()
    session.rollback = mocker.AsyncMock()
    session.refresh = mocker.AsyncMock()
    session.scalar = mocker.AsyncMock()
    return session
