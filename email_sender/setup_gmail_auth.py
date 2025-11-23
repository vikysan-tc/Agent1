# setup_gmail_auth.py
"""
Setup script to authenticate with Gmail API and get access tokens for email_sender.

Run this script once to set up Gmail API authentication.
You'll need to download OAuth2 credentials from Google Cloud Console.
"""

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def setup_gmail_auth():
    """Set up Gmail API authentication."""
    creds = None
    token_file = 'token.pickle'
    credentials_file = 'credentials.json'
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(script_dir, token_file)
    credentials_path = os.path.join(script_dir, credentials_file)
    
    # Check if credentials file exists
    if not os.path.exists(credentials_path):
        print(f"ERROR: {credentials_path} not found!")
        print("\nPlease follow these steps:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select an existing one")
        print("3. Enable the Gmail API:")
        print("   - Go to 'APIs & Services' > 'Library'")
        print("   - Search for 'Gmail API' and click 'Enable'")
        print("4. Create OAuth 2.0 credentials:")
        print("   - Go to 'APIs & Services' > 'Credentials'")
        print("   - Click 'Create Credentials' > 'OAuth client ID'")
        print("   - Choose 'Desktop app' as the application type")
        print("   - Download the credentials JSON file")
        print(f"5. Save the downloaded file as 'credentials.json' in: {script_dir}")
        return None
    
    # Load existing token if available
    if os.path.exists(token_path):
        print(f"Loading existing token from {token_path}...")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            try:
                creds.refresh(Request())
                print("Token refreshed successfully!")
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("Starting new OAuth flow...")
                creds = None
        
        if not creds:
            print("Starting OAuth flow...")
            print("A browser window will open. Please authorize the application.")
            print("Make sure you're logged into the Gmail account you want to use for sending emails.")
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials for future use
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        print(f"\nCredentials saved to {token_path}")
    
    print("\n✓ Authentication successful!")
    print(f"Access Token: {creds.token[:20]}...")
    if creds.refresh_token:
        print(f"Refresh Token: {creds.refresh_token[:20]}...")
    print(f"\nYou can now use email_sender.py to send emails!")
    
    return creds

if __name__ == '__main__':
    setup_gmail_auth()

