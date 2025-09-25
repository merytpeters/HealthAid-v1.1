"""Auth Tests"""

import uuid
import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    "account_type, extra",
    [
        ("user", {}),
        ("organization", {"name": "Test Org"}),
        ("admin", {"name": "Test Admin"}),
    ],
)
def test_register_login_logout(account_type, extra):
    """Test all user type sigu up, login and logout"""
    unique = uuid.uuid4().hex
    base_email = f"{account_type}_{unique}@example.com"
    password = "TestPassword1$"

    payload = {
        "account_type": account_type,
        "email": base_email,
        "password": password,
        **extra,
    }
    if account_type == "user":
        payload["username"] = f"{account_type}_{unique}"
        payload["full_name"] = f"{account_type.capitalize()} Full Name"

    # Register
    reg_response = client.post("/auth/register", json=payload)
    assert reg_response.status_code == 201, f"Registration failed: {reg_response.text}"
    reg_data = reg_response.json()

    # API always returns the account
    # under "user" key after to_schema unification
    assert "user" in reg_data

    # Verify email matches
    assert reg_data["user"]["email"] == base_email

    # Fix login_context value for organization:
    login_context_value = account_type
    if account_type == "organization":
        login_context_value = "organization"  # Not "org"

    login_payload = {
        "email": base_email,
        "password": password,
        "login_context": login_context_value,
    }
    login_response = client.post("/auth/login", json=login_payload)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    login_data = login_response.json()

    assert "user" in login_data
    assert login_data["user"]["email"] == base_email

    # Logout using cookies (if set)
    my_cookies = login_response.cookies
    client.cookies.update(my_cookies)
    logout_response = client.post("/auth/logout")
    assert logout_response.status_code == 200
    logout_data = logout_response.json()
    assert logout_data.get("message") == "Logout successful!"


def test_register_user_missing_email():
    """Test Missing Email"""
    payload = {
        "account_type": "user",
        "username": "missingemailuser",
        "password": "TestPassword1$",
        "full_name": "Missing Email",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 422


def test_login_wrong_password():
    """Test wrong password"""
    unique = uuid.uuid4().hex
    email = f"wrongpass_{unique}@example.com"
    payload = {
        "account_type": "user",
        "username": f"wrongpass_{unique}",
        "email": email,
        "password": "CorrectPassword1$",
        "full_name": "Wrong Password",
    }
    reg_response = client.post("/auth/register", json=payload)
    # 201 Created or 409 Conflict if duplicate
    # email already exists from previous runs
    assert reg_response.status_code in (201, 409)

    login_payload = {
        "email": email,
        "password": "IncorrectPassword!",
        "login_context": "user",
    }
    login_response = client.post("/auth/login", json=login_payload)
    assert login_response.status_code == 401


def test_login_nonexistent_user():
    """Test for nonexistent user"""
    login_payload = {
        "email": "nonexistentuser@example.com",
        "password": "SomePassword1$",
        "login_context": "user",
    }
    login_response = client.post("/auth/login", json=login_payload)
    assert login_response.status_code == 401


def test_register_user_without_organization():
    """Register user without Organization"""
    unique = uuid.uuid4().hex
    payload = {
        "account_type": "user",
        "username": f"user_no_org_{unique}",
        "email": f"user_no_org_{unique}@example.com",
        "password": "TestPassword1$",
        "full_name": "User No Org",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201, f"Registration failed: {response.text}"
    data = response.json()
    assert "user" in data
    assert data["user"]["username"] == payload["username"]
    assert data["user"]["email"] == payload["email"]


def test_register_organization():
    """Register Organization Test"""
    unique = uuid.uuid4().hex
    payload = {
        "account_type": "organization",
        "name": f"Org_{unique}",
        "email": f"org_{unique}@example.com",
        "password": "TestPassword1$",
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201, f"Registration failed: {response.text}"
    data = response.json()
    # Accept either "user" or "organization" key
    # based on API response structure
    assert "user" in data or "organization" in data
    if "organization" in data:
        assert data["organization"]["name"] == payload["name"]
        assert data["organization"]["email"] == payload["email"]
    else:
        assert data["user"]["email"] == payload["email"]
