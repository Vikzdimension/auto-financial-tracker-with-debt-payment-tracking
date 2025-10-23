import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# GOOGLE_CREDENTIALS_PATH = os.path.join(BASE_DIR, "../credentials.json")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", os.path.join(BASE_DIR, "../credentials.json"))

TOKEN_PATH = os.path.join(BASE_DIR, "../token.json")

#gmail scopes

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

#redirect

REDIRECT_URI = "http://127.0.0.1:8000/gmail/callback"

#load client config

try:
    with open(GOOGLE_CREDENTIALS_PATH) as f:
        CLIENT_CONFIG = json.load(f)
except FileNotFoundError:
    print(f"Warning: Google credentials file not found at {GOOGLE_CREDENTIALS_PATH}")
    CLIENT_CONFIG = None
except json.JSONDecodeError:
    print(f"Warning: Invalid JSON in credentials file at {GOOGLE_CREDENTIALS_PATH}")
    CLIENT_CONFIG = None