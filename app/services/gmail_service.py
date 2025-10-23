from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import re
from datetime import timezone
from app.config import GOOGLE_CREDENTIALS_PATH, TOKEN_PATH, SCOPES


def get_gmail_service(token_path: str = TOKEN_PATH):
    creds = None

    # Load creds from token.json
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            print(f"Invalid token.json, regenerating... ({e})")

    # If creds are not valid or missing, run OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Opening browser to authenticate your Google account")
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        print("Token generated and saved!")

    # timezone handling
    if creds.expiry:
        if creds.expiry.tzinfo is None:
            creds.expiry = creds.expiry.replace(tzinfo=timezone.utc)
        # Force refresh
        try:
            _ = creds.valid
        except TypeError:
            creds.expiry = None

    service = build('gmail', 'v1', credentials=creds)
    return service


def fetch_messages(service, max_results=50):
    results = service.users().messages().list(
        userId='me',
        maxResults=max_results
    ).execute()
    return results.get('messages', [])


def get_message_detail(service, msg_id):
    email = service.users().messages().get(userId='me', id=msg_id).execute()
    headers = email['payload'].get('headers', [])
    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), '')
    sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), '')
    date = next((h['value'] for h in headers if h['name'].lower() == 'date'), '')
    snippet = email.get('snippet', '')

    return {
        "subject": subject,
        "vendor": sender,
        "date": date,
        "snippet": snippet,
        "email_id": msg_id
    }


def parse_amount(text: str):
    matches = re.findall(r'₹?\$?\d+(?:,\d{3})*(?:\.\d{1,2})?', text)
    if matches:
        try:
            return float(matches[0].replace(',', '').replace('₹', '').replace('$', ''))
        except ValueError:
            return 0.0
    return 0.0
