
from fastapi import FastAPI 
from fastapi.responses import HTMLResponse

api= FastAPI()

# GET, POST, PUT, DELETE

@api.get("/")
def index():
    return HTMLResponse("<h1>Welcome to the FastAPI application!</h1>")
