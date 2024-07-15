import sys

sys.path.append("..")

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

import models
from database import SessionLocal, engine

from .auth import get_current_user, get_password_hash, verify_password

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not Found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Pydantic model for user verification during password change
class UserVerification(BaseModel):
    old_password: str
    password: str
    password2: str


# Endpoint to render the form to change user password
@router.get("/change-password", response_class=HTMLResponse)
async def edit_user_view(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        "change-password.html", {"request": request, "user": user}
    )


# Endpoint to handle the password change form submission
@router.post("/change-password", response_class=HTMLResponse)
async def user_password_change(
    request: Request,
    old_password: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_data = db.query(models.Users).filter(models.Users.id == user.get("id")).first()
    msg = "Invalid password"
    if user_data is not None:
        if password == password2 and verify_password(
            old_password, user_data.hashed_password
        ):
            user_data.hashed_password = get_password_hash(password)
            db.add(user_data)
            db.commit()
            msg = "Password updated"

    return templates.TemplateResponse(
        "change-password.html", {"request": request, "user": user, "msg": msg}
    )
