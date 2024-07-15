import sys
from datetime import timedelta

from routers.auth import get_password_hash, create_access_token, verify_password
from routers.users import get_db
from test.app_habit_test import override_get_db, TestingSessionLocal, client

sys.path.append("..")

import pytest

from starlette import status

from main import app
from models import Users

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def test_user():
    db = TestingSessionLocal()
    user = Users(
        email="example@gmail.com",
        username="example",
        first_name="example",
        last_name="example",
        hashed_password=get_password_hash("password"),  # 'password'
        is_active=True,
    )
    db.add(user)
    db.commit()
    yield user
    db.query(Users).filter(Users.id == user.id).delete()
    db.commit()
    db.close()


def test_edit_user_view_authenticated(test_user):
    token = create_access_token(
        "example", test_user.id, expires_delta=timedelta(minutes=15)
    )
    client.cookies.set("access_token", token)
    response = client.get("/users/change-password")
    assert response.status_code == status.HTTP_200_OK
    assert "change-password" in response.text


def test_change_password_success(test_user):
    token = create_access_token(
        "example", test_user.id, expires_delta=timedelta(minutes=15)
    )
    client.cookies.set("access_token", token)
    response = client.post(
        "/users/change-password",
        data={
            "old_password": "password",
            "password": "newpassword",
            "password2": "newpassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Password updated" in response.text
    db = TestingSessionLocal()
    user = db.query(Users).filter(Users.id == test_user.id).first()
    assert user is not None
    assert verify_password("newpassword", user.hashed_password)
    db.close()


def test_change_password_mismatch(test_user):
    token = create_access_token(
        "example", test_user.id, expires_delta=timedelta(minutes=15)
    )
    client.cookies.set("access_token", token)
    response = client.post(
        "/users/change-password",
        data={
            "old_password": "password",
            "password": "newpassword",
            "password2": "wrongpassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Invalid password" in response.text


def test_change_password_wrong_old_password(test_user):
    token = create_access_token(
        "example", test_user.id, expires_delta=timedelta(minutes=15)
    )
    client.cookies.set("access_token", token)
    response = client.post(
        "/users/change-password",
        data={
            "old_password": "wrongpassword",
            "password": "newpassword",
            "password2": "newpassword",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "Invalid password" in response.text
