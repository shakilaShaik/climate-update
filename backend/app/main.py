from fastapi import FastAPI
from app.db import db

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Climate Hazard API is working"}
