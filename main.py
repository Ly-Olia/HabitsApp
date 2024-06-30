from fastapi import FastAPI
import models
from database import engine
from routers import auth, habits, users
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette import status

# Create an instance of the FastAPI application
app = FastAPI()

# Create all tables in the database
models.Base.metadata.create_all(bind=engine)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")


# Define the root endpoint
@app.get("/")
async def root():
    return RedirectResponse(url="/habits", status_code=status.HTTP_302_FOUND)


# Define the health check endpoint
@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


# Include the routers for authentication, habits, and users
app.include_router(auth.router)
app.include_router(habits.router)
app.include_router(users.router)
