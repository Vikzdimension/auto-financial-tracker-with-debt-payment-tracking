import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GOOGLE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "../credentials.json")
TOKEN_PATH = os.path.join(BASE_DIR, "../token.json")

#gmail scopes

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

#redirect

REDIRECT_URI = "http://127.0.0.1:8000/gmail/callback"

#load client config

with open(GOOGLE_CREDENTIALS_PATH) as f:
    CLIENT_CONFIG = json.load(f)