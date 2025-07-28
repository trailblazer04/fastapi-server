
from fastapi import FastAPI, HTTPException, status, Depends # for error handling and status codes and request handling and dependency injection
from sqlalchemy.orm import Session # for ORM session management
from . import models, schemas, database # importing models, schemas, and database modules

# Create the database tables if they do not exist
#models.Base.metadata.create_all(bind=database.engine) # for creating Pydantic models

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint with a welcome message
@app.get("/")
def home():
    return {"message": "Welcome to the local-db-psql-fastapi app!"}

# Endpoint to add a new user
@app.post("/add", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("Received user:", user) # Debugging print statement to check received user data
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Create a new user instance
    new_user = models.User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
   
# Endpoint to get all users
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_users(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user  # SQLAlchemy instance; Pydantic with `from_attributes=True` will serialize it
