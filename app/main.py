
import psycopg2
from fastapi import FastAPI, HTTPException, status # for error handling and status codes
from contextlib import asynccontextmanager

# connect to the PostgreSQL DB - DBngin
conn = psycopg2.connect(
    host="localhost",
    port=5432, # DBngin port
    user="leo",
    password="secret12345",
    database="local_db"
)
cur = conn.cursor()

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
def add_user(name: str, email: str):
    try:
        cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
        conn.commit()
        return {"message": "User added"}
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")

@app.get("/users")
def get_users():
    cur.execute("SELECT * FROM users;")
    return {"users": cur.fetchall()}
