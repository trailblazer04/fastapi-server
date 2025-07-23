
import psycopg2
from fastapi import FastAPI, HTTPException, status, Request # for error handling and status codes and request handling
from contextlib import asynccontextmanager
from pydantic import BaseModel, EmailStr, constr # importing pydantic and emailstr and constr for validation

# connect to the PostgreSQL DB - DBngin
conn = psycopg2.connect(
    host="db",
    port=5432, # DBngin port
    user="leo",
    password="secret12345",
    database="local_db"
)
cur = conn.cursor()

# Creating a Pydantic model for user data
class User(BaseModel):
    name: constr(min_length=1, max_length=50)  # name must be at least 1 character long and at most 50 characters
    email: EmailStr  # email must be a valid email format

# FastAPI app with lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI): # replaced deprecated @app.on_event("startup")
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)
    conn.commit()
    yield # continues the app startup

    cur.close()
    conn.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"message": "Welcome to the local-db-psql-fastapi app!"}


@app.post("/add", status_code=status.HTTP_201_CREATED)
def add_user(user: User):
    try:
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s);", 
            (user.name, user.email)
        )
        conn.commit()
        return {"message": "User added"}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
def get_users():
    cur.execute("SELECT * FROM users;")
    return {"users": cur.fetchall()}
