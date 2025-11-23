"""
Email Sender Module for Greeter Agent
Sends status update emails to customers using Gmail API via noreply-sherlox@gmail.com
"""

import os
import base64
import json
import pickle
from typing import Optional, Dict, Any
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

# Try to import CRM email generator for enriched email content
try:
    from .crm_email_generator import (
        generate_ticket_created_email_body,
        generate_booking_acknowledgement_email_body,
        generate_refund_reinitiated_email_body
    )
    CRM_EMAIL_GENERATOR_AVAILABLE = True
except ImportError:
    try:
        from crm_email_generator import (
            generate_ticket_created_email_body,
            generate_booking_acknowledgement_email_body,
            generate_refund_reinitiated_email_body
        )
        CRM_EMAIL_GENERATOR_AVAILABLE = True
    except ImportError:
        CRM_EMAIL_GENERATOR_AVAILABLE = False

# Gmail API Scope - full email send access
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Configuration
SENDER_EMAIL_NO_REPLY = os.environ.get('GMAIL_SENDER_EMAIL_NO_REPLY', 'noreply-sherlox@gmail.com')
GMAIL_ACCESS_TOKEN_NO_REPLY = os.environ.get('GMAIL_ACCESS_TOKEN_NO_REPLY', '')
GMAIL_REFRESH_TOKEN_NO_REPLY = os.environ.get('GMAIL_REFRESH_TOKEN_NO_REPLY', '')
GMAIL_CLIENT_ID_NO_REPLY = os.environ.get('GMAIL_CLIENT_ID_NO_REPLY', '')
GMAIL_CLIENT_SECRET_NO_REPLY = os.environ.get('GMAIL_CLIENT_SECRET_NO_REPLY', '')
TOKEN_PICKLE_FILE = os.path.join(os.path.dirname(__file__), 'gmail_token.pickle')
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')


def _get_gmail_service():
    """
    Get authenticated Gmail service.
    Uses OAuth2 flow if credentials.json exists, otherwise uses access token.
    """
    # Try using access token first (for production)
    if GMAIL_ACCESS_TOKEN_NO_REPLY:
        try:
            service = build('gmail', 'v1', credentials=None)
            # We'll use requests directly with access token
            return None  # Signal to use token-based approach
        except Exception:
            pass
    
    # Try OAuth2 flow if credentials.json exists
    creds = None
    if os.path.exists(TOKEN_PICKLE_FILE):
        with open(TOKEN_PICKLE_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        elif os.path.exists(CREDENTIALS_FILE):
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            return None  # No credentials available
        
        with open(TOKEN_PICKLE_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    if creds:
        return build('gmail', 'v1', credentials=creds)
    return None


def _get_access_token() -> Optional[str]:
    """Get or refresh Gmail API access token."""
    if GMAIL_ACCESS_TOKEN_NO_REPLY:
        return GMAIL_ACCESS_TOKEN_NO_REPLY
    
    if GMAIL_REFRESH_TOKEN_NO_REPLY and GMAIL_CLIENT_ID_NO_REPLY and GMAIL_CLIENT_SECRET_NO_REPLY:
        try:
            response = requests.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'client_id': GMAIL_CLIENT_ID_NO_REPLY,
                    'client_secret': GMAIL_CLIENT_SECRET_NO_REPLY,
                    'refresh_token': GMAIL_REFRESH_TOKEN_NO_REPLY,
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


def send_email(
    to_email: str,
    subject: str,
    message_text: str,
    sender_email: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send an email using Gmail API.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        message_text: Email body text
        sender_email: Sender email (defaults to SENDER_EMAIL_NO_REPLY from env)
    
    Returns:
        Dict with status and message details
    """
    sender = sender_email or SENDER_EMAIL_NO_REPLY
    
    # Try OAuth2 service first
    service = _get_gmail_service()
    
    if service:
        # Use OAuth2 service
        try:
            message = MIMEText(message_text)
            message['to'] = to_email
            message['from'] = sender
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            send_result = service.users().messages().send(
                userId="me",
                body={'raw': raw_message}
            ).execute()
            
            return {
                "status": "success",
                "message_id": send_result.get('id'),
                "message": "Email sent successfully via OAuth2"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Failed to send email via OAuth2: {str(e)}"
            }
    
    # Fallback to access token method
    token = _get_access_token()
    if not token:
        return {
            "status": "error",
            "error": "Gmail access token not available. Configure GMAIL_ACCESS_TOKEN_NO_REPLY or OAuth2 credentials."
        }
    
    try:
        # Create email message
        message = MIMEText(message_text)
        message['to'] = to_email
        message['from'] = sender
        message['subject'] = subject
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Send via Gmail API using access token
        url = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'raw': raw_message
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return {
                "status": "success",
                "message_id": result.get('id'),
                "message": "Email sent successfully via access token"
            }
        else:
            return {
                "status": "error",
                "error": f"Failed to send email. HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to send email: {str(e)}"
        }


def send_ticket_created_email(
    customer_email: str,
    customer_name: str,
    ticket_reference: Optional[str] = None,
    issue_description: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send email notification when a ticket is created.
    Uses CRM API data if available to enrich email content.
    
    Args:
        customer_email: Customer's email address
        customer_name: Customer's name
        ticket_reference: Ticket reference number (optional)
        issue_description: Brief description of the issue (optional)
    
    Returns:
        Dict with status of email sending
    """
    subject = "Ticket Created - Sherlox Support"
    if ticket_reference:
        subject = f"Ticket Created - Reference: {ticket_reference}"
    
    # Use CRM email generator if available for richer content
    if CRM_EMAIL_GENERATOR_AVAILABLE:
        try:
            message = generate_ticket_created_email_body(
                customer_name=customer_name,
                ticket_reference=ticket_reference,
                issue_description=issue_description
            )
        except Exception as e:
            # Fallback to basic email if CRM generator fails
            print(f"Warning: CRM email generator failed, using basic email: {e}")
            message = _generate_basic_ticket_email(customer_name, ticket_reference, issue_description)
    else:
        message = _generate_basic_ticket_email(customer_name, ticket_reference, issue_description)
    
    return send_email(customer_email, subject, message)


def _generate_basic_ticket_email(
    customer_name: str,
    ticket_reference: Optional[str] = None,
    issue_description: Optional[str] = None
) -> str:
    """Generate basic ticket email body (fallback)."""
    message = f"""Dear {customer_name},

Thank you for contacting Sherlox Support.

We have received your request and created a support ticket for you.
"""
    
    if ticket_reference:
        message += f"\nYour ticket reference number is: {ticket_reference}\n"
    
    if issue_description:
        message += f"\nIssue: {issue_description[:200]}{'...' if len(issue_description) > 200 else ''}\n"
    
    message += """
Our team will review your request and get back to you shortly.

If you have any questions, please reply to this email with your ticket reference number.

Best regards,
Sherlox Support Team
"""
    return message


def send_booking_acknowledgement_email(
    customer_email: str,
    customer_name: str,
    booking_id: str,
    ticket_reference: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send email notification when a booking is acknowledged for refund.
    Uses CRM API data if available to enrich email content.
    
    Args:
        customer_email: Customer's email address
        customer_name: Customer's name
        booking_id: Booking ID that was acknowledged
        ticket_reference: Ticket reference number (optional)
    
    Returns:
        Dict with status of email sending
    """
    subject = f"Booking Refund Acknowledged - {booking_id}"
    
    # Use CRM email generator if available for richer content
    if CRM_EMAIL_GENERATOR_AVAILABLE:
        try:
            message = generate_booking_acknowledgement_email_body(
                customer_name=customer_name,
                booking_id=booking_id,
                ticket_reference=ticket_reference,
                customer_email=customer_email
            )
        except Exception as e:
            # Fallback to basic email if CRM generator fails
            print(f"Warning: CRM email generator failed, using basic email: {e}")
            message = _generate_basic_booking_ack_email(customer_name, booking_id, ticket_reference)
    else:
        message = _generate_basic_booking_ack_email(customer_name, booking_id, ticket_reference)
    
    return send_email(customer_email, subject, message)


def _generate_basic_booking_ack_email(
    customer_name: str,
    booking_id: str,
    ticket_reference: Optional[str] = None
) -> str:
    """Generate basic booking acknowledgement email body (fallback)."""
    message = f"""Dear {customer_name},

We have acknowledged your refund request for booking {booking_id}.
"""
    
    if ticket_reference:
        message += f"\nTicket Reference: {ticket_reference}\n"
    
    message += """
We will connect with the bank and respond on the refund status.

You will receive another email shortly with further instructions regarding your refund.

Best regards,
Sherlox Support Team
"""
    return message


def send_upi_request_email(
    customer_email: str,
    customer_name: str,
    booking_id: str,
    ticket_reference: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send email requesting UPI ID for refund processing.
    
    Args:
        customer_email: Customer's email address
        customer_name: Customer's name
        booking_id: Booking ID
        ticket_reference: Ticket reference number (optional)
    
    Returns:
        Dict with status of email sending
    """
    subject = f"UPI ID Required for Refund - Booking {booking_id}"
    
    message = f"""Dear {customer_name},

The refund for your booking {booking_id} is on hold as the UPI ID for your account is inactive.
"""
    
    if ticket_reference:
        message += f"\nTicket Reference: {ticket_reference}\n"
    
    message += """
Please provide your correct UPI ID so we can process your refund.

You can reply to this email with your UPI ID, or contact our support team.

Best regards,
Sherlox Support Team
"""
    
    return send_email(customer_email, subject, message)


def send_refund_reinitiated_email(
    customer_email: str,
    customer_name: str,
    booking_id: str,
    ticket_reference: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send email notification when refund is reinitiated.
    Uses CRM API data if available to enrich email content.
    
    Args:
        customer_email: Customer's email address
        customer_name: Customer's name
        booking_id: Booking ID
        ticket_reference: Ticket reference number (optional)
    
    Returns:
        Dict with status of email sending
    """
    subject = f"Refund Reinitiated - Booking {booking_id}"
    
    # Use CRM email generator if available for richer content
    if CRM_EMAIL_GENERATOR_AVAILABLE:
        try:
            message = generate_refund_reinitiated_email_body(
                customer_name=customer_name,
                booking_id=booking_id,
                ticket_reference=ticket_reference,
                customer_email=customer_email
            )
        except Exception as e:
            # Fallback to basic email if CRM generator fails
            print(f"Warning: CRM email generator failed, using basic email: {e}")
            message = _generate_basic_refund_reinit_email(customer_name, booking_id, ticket_reference)
    else:
        message = _generate_basic_refund_reinit_email(customer_name, booking_id, ticket_reference)
    
    return send_email(customer_email, subject, message)


def _generate_basic_refund_reinit_email(
    customer_name: str,
    booking_id: str,
    ticket_reference: Optional[str] = None
) -> str:
    """Generate basic refund reinitiated email body (fallback)."""
    message = f"""Dear {customer_name},

The refund for your booking {booking_id} has been reinitiated.
"""
    
    if ticket_reference:
        message += f"\nYou can track the refund status using ticket reference: {ticket_reference}\n"
    
    message += """
We will update the same on the bank side and keep you posted on the refund status.

Thank you for your patience.

Best regards,
Sherlox Support Team
"""
    return message

