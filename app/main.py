
import psycopg2
from fastapi import FastAPI

app = FastAPI()

conn = psycopg2.connect(
    host="localhost",
    port=5432, # DBngin port
    user="leo",
    password="secret12345",
    database="local_db"
)
cur = conn.cursor()

@app.on_event("startup")
def init():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );
    """)
    conn.commit()

@app.post("/add")
def add_user(name: str, email: str):
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s);", (name, email))
    conn.commit()
    return {"message": "User added"}

@app.get("/users")
def get_users():
    cur.execute("SELECT * FROM users;")
    return {"users": cur.fetchall()}
