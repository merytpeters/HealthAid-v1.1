"""Test For Config Settings"""
from backend.app.core.config import settings
import pytest


@pytest.fixture(scope="module")
def load_settings():
    """Fixture to load settings before running tests."""
    return settings


def test_settings_loaded():
    """Test settings"""
    assert settings.DATABASE_URL != "", "DATABASE_URL should not be empty"
    assert settings.SECRET_KEY != "", "SECRET_KEY should not be empty"
