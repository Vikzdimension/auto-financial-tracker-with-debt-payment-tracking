from fastapi import FastAPI
from app.routes import gmail_routes
from app.database import Base, engine
from app.models import Transaction
from app.services.scheduler_service import TransactionScheduler

app = FastAPI(title="Auto Finance Personal Tracker")

# Initialize database tables
Base.metadata.create_all(bind=engine)

Scheduler = TransactionScheduler()
# Include routes
app.include_router(gmail_routes.router, prefix="/gmail", tags=["Gmail"])


@app.on_event("startup")
def startup_event():
    Scheduler.start_scheduler(interval_minutes=30)

@app.on_event("shutdown")
def shutdown_event():
    Scheduler.stop_scheduler()
    
@app.get("/")
def root():
    return {"message": "Welcome to Auto Finance Personal Tracker"}

