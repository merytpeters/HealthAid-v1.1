"""User Tests"""
import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.lib.crud.user import create_user
from backend.app.schemas.user import UserCreate
from backend.app.db.session import get_db


@pytest.fixture(scope="module")
def test_db():
    """Yield a test DB session."""
    db_gen = get_db()
    db_session = next(db_gen)
    try:
        yield db_session
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


@pytest.fixture(scope="module")
def create_user_without_organization(test_db):
    """Testing Regular User without organization"""
    def _create_user():
        user_data = UserCreate(
            username="testuser4",
            email="testuser4@example.com",
            password="Testpassword4$",
            full_name="Test Monkey4"
        )
        user = create_user(
            db=test_db,
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
            full_name=user_data.full_name
        )
        assert str(user.username) == "testuser4"
        assert str(user.email) == "testuser4@example.com"
        return user
    return _create_user


def test_create_user(create_user_without_organization):
    """Test Registration"""
    create_user_fn = create_user_without_organization()
    assert create_user_fn.username == "testuser4"
    assert create_user_fn.email == "testuser4@example.com"


client = TestClient(app)


def test_register_user():
    """Test Register User"""
    unique = uuid.uuid4().hex
    payload = {
        "username": f"apitestuser3_{unique}",
        "email": f"apitestuser3_{unique}@example.com",
        "password": "testpassword3$",
        "full_name": "API Test UserMonkey3"
    }
    response = client.post("/auth/user/register", json=payload)
    print("RESPONSE STATUS:", response.status_code)
    print("RESPONSE BODY:", response.text)
    assert response.status_code == 201
    data = response.json()

    assert "user" in data
    assert "username" in data["user"], f"Response user data: {data['user']}"
    assert data["user"]["username"] == payload["username"]
    assert data["user"]["email"] == payload["email"]


def test_login():
    """Test Login"""
    unique = uuid.uuid4().hex
    register_payload = {
        "username": f"apitestuser4_{unique}",
        "email": f"apitestuser4_{unique}@example.com",
        "password": "testpassword4$",
        "full_name": "API Test UserMonkey4"
    }
    # Register the user first
    register_response = client.post(
        "/auth/user/register", json=register_payload
    )
    assert register_response.status_code == 201

    login_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"]
    }
    login_response = client.post("/auth/user/login", json=login_payload)
    print("LOGIN RESPONSE STATUS:", login_response.status_code)
    print("LOGIN RESPONSE BODY:", login_response.text)
    assert login_response.status_code == 202
    login_data = login_response.json()

    assert "access_token" in login_data
    assert login_data["token_type"] == "bearer"
