"""User Tests"""
import pytest
from backend.lib.crud.user import create_user
from backend.app.schemas.user import UserCreate
from backend.app.db.session import get_db


"""Tests For crud functions"""
@pytest.fixture(scope="module")
def db():
    # Use your test database session here
    # For example, yield from get_db() or create a test session
    yield next(get_db())

@pytest.fixture(scope="module")
def create_user_without_organization(db):
    def _create_user():
        user_data = UserCreate(
            username="testuser",
            email="testuser@example.com",
            password="testpassword",
            full_name="Test Monkey"
        )
        user = create_user(db=db, user_data=user_data)
        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        return user
    return _create_user

def test_create_user(create_user_without_organization):
    user = create_user_without_organization()
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    
    


"""Test for user routes"""    
    
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.api.routes.auth import register_user
import uuid

client = TestClient(app)

def test_register_user():
    unique = uuid.uuid4().hex
    payload = {
        "username": f"apitestuser_{unique}",
        "email": f"apitestuser_{unique}@example.com",
        "password": "testpassword",
        "full_name": "API Test UserMonkey"
    }
    response = client.post("/auth/register", json=payload)
    print("RESPONSE STATUS:", response.status_code)
    print("RESPONSE BODY:", response.text)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]