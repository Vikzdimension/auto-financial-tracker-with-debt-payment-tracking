from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
import os
from app import config

router = APIRouter()

@router.get("/auth")
def gmail_auth():
    flow = Flow.from_client_config(
        config.CLIENT_CONFIG,
        scopes=config.SCOPES,
        redirect_uri=config.REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return RedirectResponse(auth_url)

# auth callback

@router.get("/callback")
def callback(code: str):
    flow = Flow.from_client_config(
        config.CLIENT_CONFIG,
        scopes=config.SCOPES,
        redirect_uri=config.REDIRECT_URI
    )
    flow.fetch_token(code=code)

    creds = flow.credentials

    with open(config.TOKEN_PATH, "w") as f:
        f.write(creds.to_json())

    return {"message": "Gmail authorization Sucessful!"}
