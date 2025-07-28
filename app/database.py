# DB connection 

from sqlmodel import SQLModel, create_engine, Session
from .env import env 

engine = create_engine(env.DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

        