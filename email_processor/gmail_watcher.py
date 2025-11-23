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


def _get_access_token(force_refresh: bool = False) -> Optional[str]:
    """Get or refresh Gmail API access token."""
    # If we have a stored access token and not forcing refresh, try it first
    if GMAIL_ACCESS_TOKEN and not force_refresh:
        return GMAIL_ACCESS_TOKEN
    
    # Try to refresh using refresh token
    if GMAIL_REFRESH_TOKEN and GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET:
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
                new_token = data.get('access_token')
                if new_token:
                    print("Successfully refreshed Gmail access token")
                    return new_token
            else:
                print(f"Error refreshing token: HTTP {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error refreshing token: {e}")
    else:
        if not GMAIL_REFRESH_TOKEN:
            print("WARNING: GMAIL_REFRESH_TOKEN not set")
        if not GMAIL_CLIENT_ID:
            print("WARNING: GMAIL_CLIENT_ID not set")
        if not GMAIL_CLIENT_SECRET:
            print("WARNING: GMAIL_CLIENT_SECRET not set")
    
    # If we have a stored access token (even if expired), return it as fallback
    if GMAIL_ACCESS_TOKEN:
        return GMAIL_ACCESS_TOKEN
    
    return None


def _get_headers(force_refresh: bool = False) -> Dict[str, str]:
    """Get HTTP headers with authorization."""
    token = _get_access_token(force_refresh=force_refresh)
    if not token:
        raise ValueError(
            "Gmail access token not available.\n"
            "Please set one of the following:\n"
            "1. GMAIL_ACCESS_TOKEN (direct access token)\n"
            "2. GMAIL_REFRESH_TOKEN + GMAIL_CLIENT_ID + GMAIL_CLIENT_SECRET (for automatic refresh)\n"
            "Or run setup_gmail_auth.py to set up authentication."
        )
    
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
        
        # If we get a 401, try refreshing the token and retry once
        if response.status_code == 401:
            print(f"Received 401 Unauthorized for email {message_id}. Attempting to refresh token...")
            token = _get_access_token(force_refresh=True)
            if token:
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            print(f"Error fetching email {message_id}: {response.status_code}")
            return None
        
        return response.json()
    except ValueError as e:
        print(f"Authentication error fetching email {message_id}: {e}")
        return None
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
        
        # If we get a 401, try refreshing the token and retry once
        if response.status_code == 401:
            print("Received 401 Unauthorized. Attempting to refresh token...")
            # Force refresh the token
            token = _get_access_token(force_refresh=True)
            if token:
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code != 200:
            error_msg = f"Error listing messages: {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg += f" - {error_data['error'].get('message', 'Unknown error')}"
            except:
                error_msg += f" - {response.text[:200]}"
            print(error_msg)
            
            # Provide helpful error message for 401
            if response.status_code == 401:
                print("\n401 Unauthorized Error - Possible causes:")
                print("1. Gmail access token is expired or invalid")
                print("2. Gmail refresh token is expired or invalid")
                print("3. OAuth2 credentials (CLIENT_ID, CLIENT_SECRET) are incorrect")
                print("4. Required Gmail API scopes are not granted")
                print("\nTo fix:")
                print("- Run setup_gmail_auth.py to get new tokens")
                print("- Or set GMAIL_ACCESS_TOKEN and GMAIL_REFRESH_TOKEN environment variables")
                print("- Make sure Gmail API is enabled in Google Cloud Console")
            
            return []
        
        data = response.json()
        messages = data.get('messages', [])
        return [msg['id'] for msg in messages]
    except ValueError as e:
        # This is raised by _get_headers() when token is not available
        print(f"Authentication error: {e}")
        return []
    except Exception as e:
        print(f"Exception listing messages: {e}")
        return []


def _mark_email_as_read(message_id: str) -> bool:
    """Mark an email as read in Gmail by removing the UNREAD label."""
    try:
        headers = _get_headers()
        url = f"{GMAIL_API_BASE}/users/{_get_user_id()}/messages/{message_id}/modify"
        
        payload = {
            'removeLabelIds': ['UNREAD']
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        # If we get a 401, try refreshing the token and retry once
        if response.status_code == 401:
            print(f"Received 401 Unauthorized when marking email {message_id} as read. Attempting to refresh token...")
            token = _get_access_token(force_refresh=True)
            if token:
                headers = {
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json'
                }
                response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            print(f"Marked email {message_id} as read in Gmail")
            return True
        else:
            print(f"Error marking email {message_id} as read: {response.status_code} - {response.text}")
            return False
    except ValueError as e:
        print(f"Authentication error marking email {message_id} as read: {e}")
        return False
    except Exception as e:
        print(f"Exception marking email {message_id} as read: {e}")
        return False


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
                # Mark email as read in Gmail
                _mark_email_as_read(message_id)
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

