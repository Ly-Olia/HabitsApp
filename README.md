# Habit Tracker App

This is a Habit Tracker App developed to help users keep track of their habits and ensure they maintain consistency in their routines.

## Features

- **User Authentication**: Users can register, login, and manage their accounts.
- **Habit Management**: Users can create, update, and delete habits.
- **Today's Habits**: Users can view the list of their habits scheduled for the current day.
- **All Habits**: Users can view the list of all their habits.
- **Prioritize Habits**: Users can set priority levels for their habits.

## Technologies Used

- **Backend**: FastAPI
- **Database**: PostgreSQL, SQLAlchemy
- **Authentication**: OAuth2 with Password (and hashing), JWT Tokens
- **Templating**: Jinja2
- **Password Hashing**: Passlib (bcrypt)
- **Frontend**: HTML, CSS, JavaScript
- **Migrations**: Alembic
- **Testing**: pytest
  
## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Virtual Environment (optional but recommended)

### Setup

1. **Clone the repository**:
   `git clone https://github.com/Ly-Olia/HabitsApp.git`
   `cd HabitsApp`

3. **Create and activate a virtual environment**:
   `python -m venv venv`
   `source venv/bin/activate`  # On Windows use `venv\Scripts\activate`

4. **Install the dependencies**:
   `pip install -r requirements.txt`

5. **Set up the database**:

- Make sure PostgreSQL is running.
- Create a new database for the app.
- Configure the database URL in the `.env` file.

5. **Apply migrations**:
   `alembic upgrade head`

6. **Run the application**:
   `uvicorn main:app --reload`

### Usage

 - Open your browser and navigate to
   `http://127.0.0.1:8000` to access the app.
 - Use the provided API documentation at
   `http://127.0.0.1:8000/docs` for interacting with the API.

### API Endpoints

### Authentication

 - `POST /auth/token`: Obtain a token for a user.
 - `GET /auth/logout`: Logout the current user.
 - `GET /auth/register`: Render the registration page.
 - `POST /auth/register`: Register a new user.

### Habits

 - `GET /habits/today`: Get the habits scheduled for today.
 - `GET /habits`: Get a list of all habits.
 - `POST /habits`: Create a new habit.
 - `PUT /habits/{habit_id}`: Update an existing habit.
 - `DELETE /habits/{habit_id}`: Delete a habit.
 - `GET /habits/add-habit`: Render the form to add a new habit.
 - `POST /habits/add-habit`: Create a new habit.
 - `GET /habits/edit-habit/{habit_id}`: Render the form to edit an existing habit.
 - `POST /habits/edit-habit/{habit_id}`: Update an existing habit.
 - `GET /habits/delete/{habit_id}`: Delete a habit.
 - `GET /habits/complete/{habit_id}`: Mark a habit as completed.
 - `GET /habits/undo/{habit_id}`: Undo the completion of a habit.
 - `GET /habits/all`: List all habits for the current user.

### Users

 - `GET /users/change-password`: Render the form to change user password.
 - `POST /users/change-password`: Handle the password change form submission.

### Testing

The app uses pytest for testing. To run the tests, follow these steps:

1. **Install pytest**:
   `pip install pytest`

2. **Run the tests**:
   `pytest`

### Contributing
1. **Fork the repository**.
   
2. **Create a new branch**:
   `git checkout -b feature/your-feature-name`
   
3. **Make your changes**.
   
4. **Commit your changes**:
   `git commit -m 'Add some feature'`
   
5. **Push to the branch**:
   `git push origin feature/your-feature-name`
   
6. **Open a Pull Request**.




