from fastapi import FastAPI
from app.routes import gmail

app = FastAPI(title= "Auto Finance Personal Tracker")

#include routes

app.include_router(gmail.router, prefix="/gmail", tags=["Gmail"])

@app.get("/")
def root():
    return {"message": "Welcome to Auto Finance Personal Tracker"}

