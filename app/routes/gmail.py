from fastapi import APIRouter

router = APIRouter()

@router.get("/auth-check")
def gmail_auth_check():
    return {"message": "Welcome to the Gmail auth"}