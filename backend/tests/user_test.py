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
    
def test_register_user_missing_fields():
    """Test registration with missing required fields"""
    payload = {
        "username": "missingemailuser",
        "password": "Testpassword1$",
        "full_name": "Missing Email"
    }
    response = client.post("/auth/user/register", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_register_user_invalid_email():
    """Test registration with invalid email format"""
    payload = {
        "username": "invalidemailuser",
        "email": "not-an-email",
        "password": "Testpassword2$",
        "full_name": "Invalid Email"
    }
    response = client.post("/auth/user/register", json=payload)
    assert response.status_code == 422

def test_register_user_short_password():
    """Test registration with too short password"""
    payload = {
        "username": "shortpassuser",
        "email": "shortpassuser@example.com",
        "password": "short",
        "full_name": "Short Password"
    }
    response = client.post("/auth/user/register", json=payload)
    assert response.status_code == 422

def test_login_wrong_password():
    """Test login with wrong password"""
    unique = uuid.uuid4().hex
    register_payload = {
        "username": f"wrongpassuser_{unique}",
        "email": f"wrongpassuser_{unique}@example.com",
        "password": "CorrectPassword1$",
        "full_name": "Wrong Password"
    }
    register_response = client.post("/auth/user/register", json=register_payload)
    # Accept 201 or 409 (if user already exists)
    assert register_response.status_code in (201, 409)
    login_payload = {
        "email": register_payload["email"],
        "password": "WrongPassword!"
    }
    login_response = client.post("/auth/user/login", json=login_payload)
    assert login_response.status_code == 401

def test_login_nonexistent_user():
    """Test login with a non-existent user"""
    login_payload = {
        "email": "nonexistentuser@example.com",
        "password": "SomePassword1$"
    }
    login_response = client.post("/auth/user/login", json=login_payload)
    assert login_response.status_code == 401

def test_register_user_endpoint_exists():
    """Ensure the register endpoint exists and is not 404"""
    response = client.options("/auth/user/register")
    assert response.status_code != 404, "Register endpoint not found"

def test_login_user_endpoint_exists():
    """Ensure the login endpoint exists and is not 404"""
    response = client.options("/auth/user/login")
    assert response.status_code != 404, "Login endpoint not found"
    
def test_logout_user():
    """Test user logout endpoint"""
    # First, register and login a user to get tokens
    unique = uuid.uuid4().hex
    register_payload = {
        "username": f"logoutusertest_{unique}",
        "email": f"logoutusertest_{unique}@example.com",
        "password": "LogoutPassword1$",
        "full_name": "Logout User"
    }
    register_response = client.post("/auth/user/register", json=register_payload)
    assert register_response.status_code in (201, 409)
    login_payload = {
        "email": register_payload["email"],
        "password": register_payload["password"]
    }
    login_response = client.post("/auth/user/login", json=login_payload)
    assert login_response.status_code == 200
    # Extract cookies (if set)
    cookies = login_response.cookies
    # Call logout endpoint
    logout_response = client.post("/auth/logout", cookies=cookies)
    assert logout_response.status_code == 200
    # Optionally, check that cookies are deleted
    assert "access_token" not in logout_response.cookies or not logout_response.cookies.get("access_token")
    assert "refresh_token" not in logout_response.cookies or not logout_response.cookies.get("refresh_token")
