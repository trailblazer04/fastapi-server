
from fastapi import FastAPI, HTTPException, status, Depends # for error handling and status codes and request handling and dependency injection
from sqlmodel import SQLModel, Session, select #  for SQLModel ORM and session management
from .models import User # importing the User model and UserCreate schema for request validation
from .database import engine, get_session # importing the database engine and session management function
from .schemas import UserCreate, UserResponse # importing the Pydantic schemas for request and response validation


app = FastAPI()

# Dependency to get the database session
def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

# Root endpoint with a welcome message
@app.get("/")
def home():
    return {"message": "Welcome to the local-db-psql-fastapi app!"}

# Endpoint to add a new user
@app.post("/add", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    print("Received user:", user) # Debugging print statement to check received user data
    statement = select(User).where(User.email == user.email)
    existing = session.exec(statement).first() # Check if user already exists
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_user = User(name=user.name, email=user.email, address=user.address) # Create a new User instance
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user # Return the newly created user

# Endpoint to get all users
@app.get("/users/{user_id}", response_model=User)
def get_users(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id) # Fetch user by ID
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # Return the user if found
