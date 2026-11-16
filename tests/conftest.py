import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession

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
