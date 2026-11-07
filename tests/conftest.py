from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient
from starlette.routing import _DefaultLifespan

from config.db import get_db
from config.redis import set_redis_client
from main import app


@pytest.fixture
def mock_redis():
    return AsyncMock()


@pytest.fixture(autouse=True)
def set_mock_redis(mock_redis):
    set_redis_client(mock_redis)
    yield mock_redis


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def client(mock_db):
    def override_get_db():
        try:
            yield mock_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    app.router.lifespan_context = _DefaultLifespan

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
