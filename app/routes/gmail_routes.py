from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
from app.database import get_db
from app.services.gmail_service import get_gmail_service, fetch_messages, get_message_detail, parse_amount
from app.services.transaction_service import save_transaction
from app import config

router = APIRouter()

def create_oauth_flow():
    if not config.CLIENT_CONFIG:
        return None
    return Flow.from_client_config(
        config.CLIENT_CONFIG,
        scopes=config.SCOPES,
        redirect_uri=config.REDIRECT_URI
    )

@router.get("/auth")
def gmail_auth():
    flow = create_oauth_flow()
    if not flow:
        return {"error": "Google credentials not configured. Please add credentials.json file."}
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return RedirectResponse(auth_url)

@router.get("/callback")
def callback(code: str):
    flow = create_oauth_flow()
    if not flow:
        return {"error": "Google credentials not configured. Please add credentials.json file."}
    flow.fetch_token(code=code)
    with open(config.TOKEN_PATH, "w") as f:
        f.write(flow.credentials.to_json())
    return {"message": "Gmail authorization successful!"}

@router.get("/fetch")
def fetch_and_save_emails(user_id: int = 1, max_results: int = 50, db: Session = Depends(get_db)):
    service = get_gmail_service()
    messages = fetch_messages(service, max_results=max_results)
    saved = []
    for msg in messages:
        detail = get_message_detail(service, msg['id'])
        detail['amount'] = parse_amount(detail['snippet'])
        txn = save_transaction(db, user_id, detail)
        saved.append(txn)
    return {"saved_count": len(saved)}