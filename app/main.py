from fastapi import FastAPI
from app.routes import gmail_routes
from app.database import Base, engine

app = FastAPI(title="Auto Finance Personal Tracker")

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(gmail_routes.router, prefix="/gmail", tags=["Gmail"])


@app.get("/")
def root():
    return {"message": "Welcome to Auto Finance Personal Tracker"}

