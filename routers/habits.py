import sys
from typing import List

from sqlalchemy import desc

sys.path.append("..")

from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

import models
from database import SessionLocal, engine

from .auth import get_current_user

router = APIRouter(
    prefix="/habits", tags=["habits"], responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Endpoint to read all habits for the current user and day
@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(
    request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    # Get the current day of the week (0 for Monday, 1 for Tuesday, ..., 6 for Sunday)
    current_day_of_week = datetime.now().date().weekday()

    # Query habits that have the current day of the week in their 'days_of_week' attribute
    habits = (
        db.query(models.Habits)
        .filter(models.Habits.owner_id == user.get("id"))
        .filter(models.Habits.days_of_week.op("@>")([current_day_of_week]))
        .order_by(desc(models.Habits.priority))
        .all()
    )

    # Query completed habits for the current user and day
    completed_habit_ids = (
        db.query(models.Complete.habit_id)
        .filter(models.Complete.user_id == user.get("id"))
        .filter(models.Complete.complete_date == datetime.now().date())
        .all()
    )
    completed_habit_ids = [item[0] for item in completed_habit_ids]
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "habits": habits,
            "user": user,
            "completed_habit_ids": completed_habit_ids,
        },
    )


# Endpoint to render the form to add a new habit
@router.get("/add-habit", response_class=HTMLResponse)
async def add_new_habit(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        "add-habit.html", {"request": request, "user": user}
    )


# Endpoint to create a new habit
@router.post("/add-habit", response_class=HTMLResponse)
async def create_habit(
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...),
    db: Session = Depends(get_db),
    days: List[int] = Form(...),
    user=Depends(get_current_user),
):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    habit_model = models.Habits()
    habit_model.title = title
    habit_model.description = description
    habit_model.priority = priority
    habit_model.owner_id = user.get("id")
    habit_model.creation_date = datetime.now().date()

    # Store the days as an array of integers
    habit_model.days_of_week = days

    db.add(habit_model)
    db.commit()

    return RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)


# Endpoint to render the form to edit an existing habit
@router.get("/edit-habit/{habit_id}", response_class=HTMLResponse)
async def edit_habit(request: Request, habit_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    habit = db.query(models.Habits).filter(models.Habits.id == habit_id).first()
    return templates.TemplateResponse(
        "edit-habit.html", {"request": request, "habit": habit, "user": user}
    )


# Endpoint to update an existing habit
@router.post("/edit-habit/{habit_id}", response_class=HTMLResponse)
async def edit_habit_commit(
    request: Request,
    habit_id: int,
    title: str = Form(...),
    description: str = Form(...),
    priority: int = Form(...),
    days: List[int] = Form(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    habit_model = db.query(models.Habits).filter(models.Habits.id == habit_id).first()
    habit_model.title = title
    habit_model.description = description
    habit_model.priority = priority
    habit_model.days_of_week = days

    db.add(habit_model)
    db.commit()

    return RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)


# Endpoint to delete a habit
@router.get("/delete/{habit_id}")
async def delete_habit(
    habit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    habit_model = (
        db.query(models.Habits)
        .filter(models.Habits.id == habit_id)
        .filter(models.Habits.owner_id == user.get("id"))
    )

    if habit_model is None:
        return RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)
    db.query(models.Habits).filter(models.Habits.id == habit_id).delete()
    db.commit()
    return RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)


# Endpoint to mark a habit as completed
@router.get("/complete/{habit_id}", response_class=HTMLResponse)
async def complete_habit(
    habit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    habit = db.query(models.Habits).filter(models.Habits.id == habit_id).first()

    complete_model = models.Complete()
    complete_model.habit_id = habit.id
    complete_model.complete_date = datetime.now().date()
    complete_model.user_id = user.get("id")

    db.add(complete_model)
    db.commit()

    return RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)


# Endpoint to undo the completion of a habit
@router.get("/undo/{habit_id}", response_class=HTMLResponse)
async def undo_completion(
    habit_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)
):

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    completion_entry = (
        db.query(models.Complete)
        .filter(
            models.Complete.habit_id == habit_id,
            models.Complete.complete_date == datetime.now().date(),
        )
        .first()
    )

    if completion_entry:
        db.delete(completion_entry)
        db.commit()

    return RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)


# Endpoint to list all habits for the current user
@router.get("/all", response_class=HTMLResponse)
async def list_all_habits(
    request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    habits = (
        db.query(models.Habits)
        .filter(models.Habits.owner_id == user.get("id"))
        .order_by(desc(models.Habits.priority))
        .all()
    )

    return templates.TemplateResponse(
        "all-habits.html", {"request": request, "habits": habits, "user": user}
    )
