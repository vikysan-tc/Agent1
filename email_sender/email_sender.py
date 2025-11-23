from __future__ import print_function
import base64
import os
import sys
import argparse
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Gmail API Scope - full email send access
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def gmail_authenticate():
    """Authenticate with Gmail API using OAuth2."""
    creds = None
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(script_dir, 'token.pickle')
    credentials_path = os.path.join(script_dir, 'credentials.json')

    # token.pickle stores the user's access and refresh tokens
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, prompt login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                print("Starting new OAuth flow...")
                creds = None
        
        if not creds:
            if not os.path.exists(credentials_path):
                print(f"ERROR: {credentials_path} not found!")
                print("Please run setup_gmail_auth.py first to set up Gmail authentication.")
                return None
            
            print("Starting OAuth flow...")
            print("A browser window will open. Please authorize the application.")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
        print("Authentication successful!")

    return build('gmail', 'v1', credentials=creds)


def send_email(service, sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    send_result = service.users().messages().send(
        userId="me",
        body={'raw': raw_message}
    ).execute()

    print(f"Message sent successfully! Message ID: {send_result['id']}")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Send email using Gmail API')
    parser.add_argument('--recipient', '-r', 
                       help='Recipient email address (must match customer email from greeter_agent)',
                       default=os.environ.get('CUSTOMER_EMAIL'))
    parser.add_argument('--sender', '-s',
                       help='Sender email address',
                       default=os.environ.get('SENDER_EMAIL', 'your_email@gmail.com'))
    parser.add_argument('--subject', 
                       help='Email subject',
                       default=os.environ.get('EMAIL_SUBJECT', 'Gmail API OAuth Test'))
    parser.add_argument('--body',
                       help='Email body text',
                       default=os.environ.get('EMAIL_BODY', 'This is a test email sent using Gmail API and OAuth 2.0!'))
    
    args = parser.parse_args()
    
    # Validate that recipient email is provided
    if not args.recipient:
        print("ERROR: Recipient email is required!")
        print("Please provide it via:")
        print("  1. Command line: --recipient <email> or -r <email>")
        print("  2. Environment variable: CUSTOMER_EMAIL")
        print("\nThe recipient email must match the customer email from greeter_agent POST call.")
        sys.exit(1)
    
    recipient_email = args.recipient
    sender_email = args.sender
    subject = args.subject
    body = args.body
    
    print(f"Sending email to: {recipient_email}")
    print(f"Subject: {subject}")
    
    service = gmail_authenticate()
    if service:
        send_email(service, sender_email, recipient_email, subject, body)
    else:
        print("ERROR: Failed to authenticate with Gmail API")
        sys.exit(1)