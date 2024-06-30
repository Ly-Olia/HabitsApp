from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, ARRAY
from sqlalchemy.orm import relationship
from database import Base


# Define the Users model
class Users(Base):
    __tablename__ = "users"

    # Columns in the users table
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # Relationships with other tables
    habits = relationship("Habits", back_populates="owner")
    completed_habits = relationship("Complete", back_populates="user")


# Define the Habits model
class Habits(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    creation_date = Column(Date)
    days_of_week = Column(Integer, ARRAY(Integer))

    owner = relationship("Users", back_populates="habits")
    completes = relationship("Complete", back_populates="habit")


# Define the Complete model
class Complete(Base):
    __tablename__ = "complete"

    id = Column(Integer, primary_key=True, autoincrement=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    complete_date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    habit = relationship("Habits", back_populates="completes")
    user = relationship("Users", back_populates="completed_habits")
