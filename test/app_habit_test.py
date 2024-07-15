from datetime import datetime, timedelta
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models import Habits, Users, Complete
from routers.auth import get_current_user, create_access_token
from database import Base
from main import app
from routers.habits import get_db

# Define the test database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Vkkh1112!@localhost/testHabitdb"

# Create a new SQLAlchemy engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a new session factory bound to the test database engine
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create all tables in the test database
Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Dependency override for getting a test database session.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user(user_id: int):
    """
    Dependency override for getting a current test user.
    """

    def _override_get_current_user():
        return {
            "id": user_id,
            "username": "example",
            "email": "example@gmail.com",
            "first_name": "example",
            "last_name": "example",
            "hashed_password": "12345",
            "is_active": True,
        }

    return _override_get_current_user


# Override dependencies in the FastAPI app
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture
def create_test_user():
    """
    Fixture to create and yield a test user, and clean up after the test.
    """
    user = Users(
        email="example@gmail.com",
        username="example",
        first_name="example",
        last_name="example",
        hashed_password="12345",
        is_active=True,
    )
    with TestingSessionLocal() as db:
        db.add(user)
        db.commit()
        app.dependency_overrides[get_current_user] = override_get_current_user(user.id)
        yield user

        # Clean up: delete the test user
        db.query(Users).filter(Users.id == user.id).delete()
        db.commit()


@pytest.fixture
def create_test_habit(create_test_user: Users):
    """
    Fixture to create and yield a test habit, and clean up after the test.
    """
    db = TestingSessionLocal()
    habit = Habits(
        title="Habit1",
        description="description1",
        priority=5,
        owner_id=create_test_user.id,
        creation_date=datetime.now().date(),
        days_of_week=[datetime.now().weekday()],  # Current day of the week
    )
    db.add(habit)
    db.commit()
    yield habit

    # Clean up: delete the test habit
    with engine.connect() as connection:
        connection.execute(text(f"DELETE FROM habits WHERE id = {habit.id};"))
        connection.commit()
    db.close()


@pytest.fixture
def create_test_completed_habit(create_test_user: Users, create_test_habit: Habits):
    """
    Fixture to create and yield a test completed habit, and clean up after the test.
    """
    db = TestingSessionLocal()
    completed_habit = Complete(
        habit_id=create_test_habit.id,
        user_id=create_test_user.id,
        complete_date=datetime.now().date(),
    )
    db.add(completed_habit)
    db.commit()
    yield completed_habit

    # Clean up: delete the completed habit
    with engine.connect() as connection:
        connection.execute(
            text(f"DELETE FROM complete WHERE id = {completed_habit.id};")
        )
        connection.commit()
    db.close()


def test_read_all_authenticated(create_test_habit: Habits):
    """
    Test to read all habits for an authenticated user.
    """
    response = client.get("/habits")
    assert response.status_code == status.HTTP_200_OK
    html_content = response.content.decode("utf-8")
    assert create_test_habit.title in html_content


def test_create_habit(create_test_user: Users):
    """
    Test to create a new habit.
    """
    response = client.post(
        "/habits/add-habit",
        data={
            "title": "New Habit",
            "description": "New Description",
            "priority": 4,
            "days": [0, 1, 2, 3, 4, 5, 6],
        },
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify the habit was created in the database
    db = TestingSessionLocal()
    habit = db.query(Habits).filter(Habits.title == "New Habit").first()
    assert habit is not None
    assert habit.owner_id == create_test_user.id
    assert habit.creation_date == datetime.now().date()
    assert habit.title == "New Habit"
    assert habit.description == "New Description"
    assert habit.priority == 4
    assert habit.days_of_week == [0, 1, 2, 3, 4, 5, 6]

    # Clean up: delete the test habit
    with engine.connect() as connection:
        connection.execute(text(f"DELETE FROM habits WHERE id = {habit.id};"))
        connection.commit()
    db.close()


def test_edit_habit(create_test_user: Users, create_test_habit: Habits):
    """
    Test to edit an existing habit.
    """
    response = client.post(
        f"/habits/edit-habit/{create_test_habit.id}",
        data={
            "title": "Updated Habit",
            "description": "Updated Description",
            "priority": 3,
            "days": [1, 2, 3],
        },
    )
    assert response.status_code == status.HTTP_200_OK

    # Verify the habit was updated in the database
    db = TestingSessionLocal()
    habit = db.query(Habits).filter(Habits.id == create_test_habit.id).first()
    assert habit is not None
    assert habit.title == "Updated Habit"
    assert habit.description == "Updated Description"
    assert habit.owner_id == create_test_user.id
    assert habit.creation_date == datetime.now().date()
    assert habit.priority == 3
    assert habit.days_of_week == [1, 2, 3]

    # Clean up: delete the test habit
    with engine.connect() as connection:
        connection.execute(text(f"DELETE FROM habits WHERE id = {habit.id};"))
        connection.commit()
    db.close()


def test_delete_habit(create_test_user: Users, create_test_habit: Habits):
    """
    Test to delete an existing habit.
    """
    response = client.get(f"/habits/delete/{create_test_habit.id}")
    assert response.status_code == status.HTTP_200_OK

    # Verify the habit was deleted from the database
    db = TestingSessionLocal()
    habit = db.query(Habits).filter(Habits.id == create_test_habit.id).first()
    assert habit is None
    db.close()


def test_complete_habit(create_test_user: Users, create_test_habit: Habits):
    """
    Test to mark a habit as completed.
    """
    response = client.get(f"/habits/complete/{create_test_habit.id}")
    assert response.status_code == status.HTTP_200_OK

    # Verify the habit completion was recorded in the database
    db = TestingSessionLocal()
    completed = (
        db.query(Complete).filter(Complete.habit_id == create_test_habit.id).first()
    )
    assert completed is not None
    assert completed.habit_id == create_test_habit.id
    assert completed.complete_date == datetime.now().date()
    assert completed.user_id == create_test_user.id
    db.close()


def test_undo_completion(
    create_test_user: Users, create_test_completed_habit: Complete
):
    """
    Test to undo a habit completion.
    """
    response = client.get(f"/habits/undo/{create_test_completed_habit.habit_id}")
    assert response.status_code == status.HTTP_200_OK

    # Verify the habit completion was undone in the database
    db = TestingSessionLocal()
    completed = (
        db.query(Complete)
        .filter(Complete.habit_id == create_test_completed_habit.habit_id)
        .filter(Complete.complete_date == datetime.now().date())
        .first()
    )
    assert completed is None
    db.close()


def test_list_all_habits(create_test_user: Users, create_test_habit: Habits):
    """
    Test to list all habits for a user.
    """
    response = client.get("/habits/all")
    assert response.status_code == status.HTTP_200_OK
    html_content = response.content.decode("utf-8")
    assert create_test_habit.title in html_content
