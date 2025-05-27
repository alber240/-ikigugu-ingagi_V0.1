import pytest
from app import app  # ✅ Ensure correct import

@pytest.fixture
def client():
    """ ✅ Creates a test client to interact with Flask """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_successful_login(client):
    """ ✅ Test valid login credentials """
    data = {"username": "admin", "password": "securepassword"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 200
    assert "token" in response.json  # ✅ Check if a token is returned

def test_invalid_login(client):
    """ ❌ Test login failure with incorrect credentials """
    data = {"username": "wronguser", "password": "wrongpassword"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 401  # ✅ Should return Unauthorized error
    assert "error" in response.json
    assert response.json["error"] == "Invalid username or password"

def test_missing_username(client):
    """ ❌ Test login failure with missing username """
    data = {"password": "securepassword"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 400  # ✅ Should return Bad Request
    assert "error" in response.json
    assert response.json["error"] == "Username is required"

def test_missing_password(client):
    """ ❌ Test login failure with missing password """
    data = {"username": "admin"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == 400  # ✅ Should return Bad Request
    assert "error" in response.json
    assert response.json["error"] == "Password is required"

def test_invalid_token_access(client):
    """ ❌ Test accessing a protected route with an invalid token """
    headers = {"Authorization": "Bearer fake_token"}
    response = client.get("/auth/protected-route", headers=headers)
    assert response.status_code == 403  # ✅ Should return Forbidden error
    assert "error" in response.json
    assert response.json["error"] == "Invalid or expired token"
