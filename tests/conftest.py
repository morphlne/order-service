from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from config.db import get_db
from main import app
from services import user_service


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

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def clean_emails():
    user_service.emails.clear()
    yield
