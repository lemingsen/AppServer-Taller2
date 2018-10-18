import pytest
import appserver
from config import TestingConfig


@pytest.fixture
def client():
    app = appserver.create_app(TestingConfig)
    client = app.test_client()
    yield client
