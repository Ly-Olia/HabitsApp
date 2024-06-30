from datetime import datetime, timedelta
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models import Users
from main import app
from routers.auth import get_db, create_access_token, authenticate_user
from test.app_test import TestingSessionLocal, client, override_get_db

# Override the get_db dependency to use the test database session
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def create_test_user():
    """
    Fixture to create and yield a test user, and clean up after the test.
    """
    user = Users(
        email='example@gmail.com', username='example',
        first_name='example', last_name='example',
        hashed_password='$2b$12$KXQKk5Y3/MQksOHXbEdrO.tiDQyZDHe9FeP.D6CM7IMmCck30h7NK',  # 'password'
        is_active=True
    )
    with TestingSessionLocal() as db:
        db.add(user)
        db.commit()

        yield user

        # Clean up: delete the test user
        db.query(Users).filter(Users.id == user.id).delete()
        db.commit()


def test_register_user_creates_user_successfully():
    """
    Test the user registration endpoint to ensure a new user is created successfully.
    """
    response = client.post("/auth/register", data={
        "email": "newuser@example.com",
        "username": "newuser",
        "firstname": "New",
        "lastname": "User",
        "password": "newpassword",
        "password2": "newpassword"
    })
    assert response.status_code == status.HTTP_200_OK

    # Verify that the user was created in the database
    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.username == "newuser").first()
    assert user is not None
    assert user.email == "newuser@example.com"
    assert user.username == "newuser"
    assert user.first_name == "New"
    assert user.last_name == "User"

    # Clean up: delete the test user
    db.query(Users).filter(Users.id == user.id).delete()
    db.commit()
    db.close()


def test_logout_removes_access_token_cookie(create_test_user):
    """
    Test the user logout endpoint to ensure the access token cookie is removed.
    """
    token = create_access_token("example", create_test_user.id)
    client.cookies.set("access_token", token)
    response = client.get("/auth/logout")
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" not in response.cookies
