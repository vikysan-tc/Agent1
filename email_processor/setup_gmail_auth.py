# setup_gmail_auth.py
"""
Setup script to authenticate with Gmail API and get access tokens.

Run this script once to set up Gmail API authentication.
You'll need to download OAuth2 credentials from Google Cloud Console.
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',  # For sending reply emails
    'https://www.googleapis.com/auth/gmail.modify'  # For marking emails as read
]

def setup_gmail_auth():
    """Set up Gmail API authentication."""
    creds = None
    token_file = 'token.pickle'
    credentials_file = 'credentials.json'
    
    # Check if credentials file exists
    if not os.path.exists(credentials_file):
        print(f"ERROR: {credentials_file} not found!")
        print("\nPlease:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create/select a project")
        print("3. Enable Gmail API")
        print("4. Create OAuth 2.0 credentials (Desktop app)")
        print("5. Download credentials and save as 'credentials.json' in this directory")
        return None
    
    # Load existing token if available
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting OAuth flow...")
            print("A browser window will open. Please authorize the application.")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
        print(f"Credentials saved to {token_file}")
    
    print("\nAuthentication successful!")
    print(f"Access Token: {creds.token[:20]}...")
    print(f"Refresh Token: {creds.refresh_token[:20] if creds.refresh_token else 'N/A'}...")
    
    # Print environment variable commands
    print("\nSet these environment variables:")
    print(f"export GMAIL_ACCESS_TOKEN=\"{creds.token}\"")
    if creds.refresh_token:
        print(f"export GMAIL_REFRESH_TOKEN=\"{creds.refresh_token}\"")
    
    return creds

if __name__ == '__main__':
    setup_gmail_auth()

