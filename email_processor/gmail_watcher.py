# gmail_watcher.py
"""
Gmail Watcher for IBM Watsonx Orchestrate

This module handles Gmail API integration to watch for new emails
sent to the configured email address (reachus.sherlox@gmail.com).

It uses Gmail API to:
1. Watch for new messages
2. Fetch email content
3. Process emails using the email_processor tools
4. Send processed payloads to another agent

Setup Requirements:
1. Gmail API credentials (OAuth2)
2. Gmail API enabled in Google Cloud Console
3. OAuth2 client ID and secret
4. Access token with Gmail API scope
"""

import os
import json
import base64
import time
from typing import Dict, Any, Optional, List
import requests
from email.utils import parseaddr
from email.parser import Parser
import re
from dotenv import load_dotenv
load_dotenv()

# Configuration from environment variables
GMAIL_WATCH_EMAIL = os.environ.get('GMAIL_WATCH_EMAIL', 'reachus.sherlox@gmail.com')
GMAIL_ACCESS_TOKEN = os.environ.get('GMAIL_ACCESS_TOKEN', '')
GMAIL_REFRESH_TOKEN = os.environ.get('GMAIL_REFRESH_TOKEN', '')
GMAIL_CLIENT_ID = os.environ.get('GMAIL_CLIENT_ID', '')
GMAIL_CLIENT_SECRET = os.environ.get('GMAIL_CLIENT_SECRET', '')
GMAIL_API_BASE = 'https://gmail.googleapis.com/gmail/v1'
AGENT_WEBHOOK_URL = os.environ.get('AGENT_WEBHOOK_URL', '')
POLL_INTERVAL = int(os.environ.get('GMAIL_POLL_INTERVAL', '60'))  # Poll every 60 seconds

# Store for processed email IDs to avoid duplicates
PROCESSED_EMAILS_FILE = os.path.join(os.path.dirname(__file__), 'processed_emails.json')


def _load_processed_emails() -> set:
    """Load set of processed email IDs."""
    try:
        if os.path.exists(PROCESSED_EMAILS_FILE):
            with open(PROCESSED_EMAILS_FILE, 'r') as f:
                data = json.load(f)
                return set(data.get('processed_ids', []))
    except Exception:
        pass
    return set()


def _save_processed_email(email_id: str):
    """Save processed email ID."""
    try:
        processed = _load_processed_emails()
        processed.add(email_id)
        with open(PROCESSED_EMAILS_FILE, 'w') as f:
            json.dump({'processed_ids': list(processed)}, f)
    except Exception:
        pass


def _get_access_token() -> Optional[str]:
    """Get or refresh Gmail API access token."""
    if GMAIL_ACCESS_TOKEN:
        return GMAIL_ACCESS_TOKEN
    
    if GMAIL_REFRESH_TOKEN and GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET:
        # Refresh the token
        try:
            response = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'client_id': GMAIL_CLIENT_ID,
                    'client_secret': GMAIL_CLIENT_SECRET,
                    'refresh_token': GMAIL_REFRESH_TOKEN,
                    'grant_type': 'refresh_token'
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('access_token')
        except Exception as e:
            print(f"Error refreshing token: {e}")
    
    return None


def _get_headers() -> Dict[str, str]:
    """Get HTTP headers with authorization."""
    token = _get_access_token()
    if not token:
        raise ValueError("Gmail access token not available. Set GMAIL_ACCESS_TOKEN or configure OAuth2.")
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


def _get_user_id() -> str:
    """Get Gmail user ID (usually 'me' for authenticated user)."""
    return 'me'


def _fetch_email_content(message_id: str) -> Optional[Dict[str, Any]]:
    """Fetch full email content from Gmail API."""
    try:
        headers = _get_headers()
        url = f"{GMAIL_API_BASE}/users/{_get_user_id()}/messages/{message_id}?format=full"
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Error fetching email {message_id}: {response.status_code}")
            return None
        
        return response.json()
    except Exception as e:
        print(f"Exception fetching email {message_id}: {e}")
        return None


def _parse_email_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
    """Parse Gmail API message format into structured email data."""
    payload = message_data.get('payload', {})
    headers = payload.get('headers', [])
    
    # Extract headers
    header_dict = {h['name'].lower(): h['value'] for h in headers}
    from_header = header_dict.get('from', '')
    to_header = header_dict.get('to', '')
    subject = header_dict.get('subject', '')
    
    # Extract email body
    email_text = ''
    
    def extract_body(part):
        """Recursively extract body from email parts."""
        body = ''
        if part.get('body', {}).get('data'):
            data = part['body']['data']
            try:
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
            except Exception:
                pass
        
        if part.get('parts'):
            for subpart in part['parts']:
                body += extract_body(subpart)
        
        return body
    
    email_text = extract_body(payload)
    
    # Extract date header
    date_header = header_dict.get('date', '')
    
    return {
        'from': from_header,
        'to': to_header,
        'subject': subject,
        'date': date_header,
        'body': email_text,
        'message_id': message_data.get('id', ''),
        'thread_id': message_data.get('threadId', '')
    }


def _list_messages(query: str = '', max_results: int = 10) -> List[str]:
    """List message IDs matching the query."""
    try:
        headers = _get_headers()
        url = f"{GMAIL_API_BASE}/users/{_get_user_id()}/messages"
        params = {
            'q': query,
            'maxResults': max_results
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            print(f"Error listing messages: {response.status_code}")
            return []
        
        data = response.json()
        messages = data.get('messages', [])
        return [msg['id'] for msg in messages]
    except Exception as e:
        print(f"Exception listing messages: {e}")
        return []


def _process_new_emails():
    """Process new emails sent to the watch email address."""
    # Query for emails sent to the watch email
    query = f'to:{GMAIL_WATCH_EMAIL} is:unread'
    
    # Get list of unread messages
    message_ids = _list_messages(query, max_results=50)
    
    processed = _load_processed_emails()
    new_emails = [msg_id for msg_id in message_ids if msg_id not in processed]
    
    if not new_emails:
        return
    
    print(f"Found {len(new_emails)} new email(s) to process")
    
    for message_id in new_emails:
        try:
            # Fetch email content
            message_data = _fetch_email_content(message_id)
            if not message_data:
                continue
            
            # Parse email
            email_data = _parse_email_message(message_data)
            
            # Check if email is actually sent to our watch address
            to_addresses = email_data.get('to', '').lower()
            if GMAIL_WATCH_EMAIL.lower() not in to_addresses:
                _save_processed_email(message_id)
                continue
            
            # Process email using the email processor functions
            # Import processing functions (not the @tool decorated versions)
            import sys
            import importlib.util
            processor_path = os.path.join(os.path.dirname(__file__), "email_processor.py")
            spec = importlib.util.spec_from_file_location("email_processor_module", processor_path)
            processor_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(processor_module)
            
            # Use process_and_send_email which includes validation and reply logic
            result = processor_module.process_and_send_email(
                email_text=email_data['body'],
                from_header=email_data['from'],
                subject=email_data['subject'],
                to_header=email_data['to'],
                date_header=email_data.get('date', ''),
                original_message_id=email_data.get('message_id', message_id),
                thread_id=email_data.get('thread_id', '')
            )
            
            if result.get('status') in ['success', 'partial']:
                print(f"Successfully processed email {message_id}")
                _save_processed_email(message_id)
            else:
                print(f"Failed to process email {message_id}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"Error processing email {message_id}: {e}")
            # Mark as processed to avoid infinite retries
            _save_processed_email(message_id)


def watch_emails():
    """Main loop to watch for new emails."""
    print(f"Starting Gmail watcher for {GMAIL_WATCH_EMAIL}")
    print(f"Polling interval: {POLL_INTERVAL} seconds")
    
    if not _get_access_token():
        print("ERROR: Gmail access token not available!")
        print("Please set GMAIL_ACCESS_TOKEN or configure OAuth2 credentials.")
        return
    
    while True:
        try:
            _process_new_emails()
        except Exception as e:
            print(f"Error in watch loop: {e}")
        
        time.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    watch_emails()

