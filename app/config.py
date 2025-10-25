import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, "../token.json")

# Gmail scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Redirect URI
REDIRECT_URI = "http://127.0.0.1:8000/gmail/callback"

<<<<<<< HEAD
# Client config from environment variables
CLIENT_CONFIG = {
    "installed": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
    }
} if os.getenv("GOOGLE_CLIENT_ID") else None
=======
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
>>>>>>> main
