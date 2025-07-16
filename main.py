
from fastapi import FastAPI

app= FastAPI()

item = []

# GET, POST, PUT, DELETE

@app.get("/")
def index():
    return {"message": "Hello, World!"}

@app.get("/")
def create_item(item: str)