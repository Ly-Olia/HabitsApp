import sys

import jwt as jwt
from starlette.responses import RedirectResponse

# Adding the parent directory to the sys.path to allow imports from sibling modules
sys.path.append("..")

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

# Secret key and algorithm used for JWT encoding/decoding
SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

# Setting up the Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Initializing the bcrypt context for password hashing
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Creating all tables defined in the models
models.Base.metadata.create_all(bind=engine)

# OAuth2PasswordBearer instance to handle token URL
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# Setting up the API router with prefix and tags
router = APIRouter(
    prefix="/auth", tags=["auth"], responses={401: {"user": "Not authorized"}}
)


# Class to handle the login form
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    # Method to create OAuth form from request
    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("password")


# Dependency function to get a database session
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Function to hash the password
def get_password_hash(password):
    return bcrypt_context.hash(password)


# Function to verify the password
def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


# Function to authenticate the user
def authenticate_user(username: str, password: str, db):
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Function to create a JWT access token
def create_access_token(
    username: str, user_id: int, expires_delta: Optional[timedelta] = None
):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# Function to get the current user from the request
async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            logout(request)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(satus_code=404, detail="Not Found")


# Endpoint to handle login and return a token
@router.post("/token")
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = timedelta(minutes=60)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)

    response.set_cookie(key="access_token", value=token, httponly=True)
    return True


# Endpoint to render the authentication page
@router.get("/", response_class=HTMLResponse)
async def authenticationpage(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Endpoint to handle login form submission
@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(
            response=response, form_data=form, db=db
        )
        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse(
                "login.html", {"request": request, "msg": msg}
            )
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse(
            "login.html", {"request": request, "msg": msg}
        )


# Endpoint to handle logout
@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse(
        "login.html", {"request": request, "msg": msg}
    )
    response.delete_cookie(key="access_token")
    return response


# Endpoint to render the registration page
@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Endpoint to handle user registration
@router.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    email: str = Form(...),
    username: str = Form(...),
    firstname: str = Form(...),
    lastname: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    validation1 = (
        db.query(models.Users).filter(models.Users.username == username).first()
    )
    validation2 = db.query(models.Users).filter(models.Users.email == email).first()

    if password != password2 or validation1 is not None or validation2 is not None:
        msg = "Invalid registration request"
        return templates.TemplateResponse(
            "register.html", {"request": request, "msg": msg}
        )

    user_model = models.Users()
    user_model.username = username
    user_model.email = email
    user_model.first_name = firstname
    user_model.last_name = lastname

    hash_password = get_password_hash(password)
    user_model.hashed_password = hash_password
    user_model.is_active = True

    db.add(user_model)
    db.commit()

    msg = "User successfully created"
    return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
