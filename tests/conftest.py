import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activity database before each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)

@pytest.fixture
def client():
    """Provide a TestClient for API tests."""
    return TestClient(app)
