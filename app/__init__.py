# create_db.py

from sqlmodel import SQLModel
from app.database import engine
from app import models  # make sure your models are defined

if __name__ == "__main__":
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully.")
    print("You can now run your FastAPI app with 'uvicorn app.main:app --reload'")
    print("Visit http://localhost:8000/docs to interact with the API.")
    print("Enjoy your local-db-psql-fastapi app!")
else:
    print("This script is intended to be run directly, not imported.")
    print("Use 'python create_db.py' to create the database tables.")
    print("If you want to run the FastAPI app, use 'uvicorn app.main:app --reload'")
    print("Visit http://localhost:8000/docs to interact with the API.")
    print("Enjoy your local-db-psql-fastapi app!")