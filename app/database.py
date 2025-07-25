# DB connection 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .env import env 

engine = create_engine(env.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()