# email_processor.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import re
import json
import base64
from typing import Optional, Dict, Any, List
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import os
import datetime

# Gmail API configuration
GMAIL_WATCH_EMAIL = os.environ.get('GMAIL_WATCH_EMAIL', 'reachus.sherlox@gmail.com')
AGENT_WEBHOOK_URL = os.environ.get('AGENT_WEBHOOK_URL', '')  # URL to send processed emails to another agent
AGENT_WEBHOOK_URL_LOCAL = os.environ.get('AGENT_WEBHOOK_URL_LOCAL', 'http://localhost:5000/webhook')  # Local greeter agent webhook
AGENT_WEBHOOK_URL_PRODUCTION = os.environ.get('AGENT_WEBHOOK_URL_PRODUCTION', '')  # Production greeter agent webhook
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'local').lower()  # 'local' or 'production'
GMAIL_API_BASE = os.environ.get('GMAIL_API_BASE', 'https://gmail.googleapis.com/gmail/v1')
GMAIL_REPLY_EMAIL = os.environ.get('GMAIL_REPLY_EMAIL', 'reachus.sherlox@gmail.com')  # Email to send replies from
GMAIL_ACCESS_TOKEN = os.environ.get('GMAIL_ACCESS_TOKEN', '')
GMAIL_REFRESH_TOKEN = os.environ.get('GMAIL_REFRESH_TOKEN', '')
GMAIL_CLIENT_ID = os.environ.get('GMAIL_CLIENT_ID', '')
GMAIL_CLIENT_SECRET = os.environ.get('GMAIL_CLIENT_SECRET', '')

# File to save payloads when webhook is not available
PAYLOADS_FILE = os.path.join(os.path.dirname(__file__), 'saved_payloads.json')


def _extract_email_address(text: str) -> Optional[str]:
    """Extract the first valid email address from text."""
    emails = re.findall(r'[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}', text)
    return emails[0] if emails else None


def _extract_phone_number(text: str) -> Optional[str]:
    """Extract the first phone number from text."""
    phones = re.findall(r'\+?\d[\d\s\-\(\)]{6,}\d', text)
    if phones:
        # Clean up the phone number
        phone = phones[0].strip()
        return phone
    return None


def _extract_name(email_text: str, from_header: str = "") -> Optional[str]:
    """Extract customer name from email text or from header."""
    name_val = None
    
    # Try to extract from "From" header first
    if from_header:
        name, email = parseaddr(from_header)
        if name:
            name_val = name.strip()
    
    # Try explicit patterns in email body
    if not name_val:
        m = re.search(r"\bI(?:'m| am) ([A-Z][A-Za-z\s'`\-\.]{1,60})", email_text)
        if m:
            name_val = m.group(1).strip()
    
    # Fallback: look for signature lines
    if not name_val:
        sig = re.search(r'(?:Regards|Best|Thanks|Sincerely)[\,\s]*\n\s*([A-Z][A-Za-z\s\-\.]{1,60})', email_text, re.IGNORECASE)
        if sig:
            name_val = sig.group(1).strip()
    
    # Try to find name at the beginning of email
    if not name_val:
        lines = email_text.splitlines()
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and not re.search(r'[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}', line):
                # Check if it looks like a name (starts with capital, 2-60 chars, no special chars except spaces/hyphens)
                if re.match(r'^[A-Z][A-Za-z\s\'\-\.]{1,60}$', line):
                    name_val = line
                    break
    
    return name_val


def _extract_issue_description(email_text: str) -> str:
    """Extract issue description by removing greeting/signature and contact info lines."""
    lines = [l.strip() for l in email_text.splitlines()]
    body_lines = []
    
    for ln in lines:
        if not ln:
            continue
        # Skip common greetings
        if re.match(r'^(hi|hello|dear|good morning|good afternoon|good evening)\b', ln, re.IGNORECASE):
            continue
        # Skip signature markers
        if re.match(r'^(regards|best|thanks|thank you|sincerely|yours)\b', ln, re.IGNORECASE):
            break
        # Skip lines containing email
        if re.search(r'[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}', ln):
            continue
        # Skip lines containing phone
        if re.search(r'\+?\d[\d\s\-\(\)]{6,}\d', ln):
            continue
        # Skip name intro lines
        if re.match(r"^I(?:'m| am) ", ln, re.IGNORECASE):
            continue
        # Skip common email headers/footers
        if re.match(r'^(from:|to:|subject:|sent:|date:)', ln, re.IGNORECASE):
            continue
        body_lines.append(ln)
    
    issue_description = ' '.join(body_lines).strip()
    if not issue_description:
        # Fallback to whole text if heuristic removed too much
        issue_description = email_text.strip()
    
    return issue_description


def _determine_priority(email_text: str, subject: str = "") -> str:
    """Determine priority based on keywords in email text and subject."""
    high_priority_keywords = [
        'urgent', 'emergency', 'critical', 'asap', 'immediately', 
        'refund', 'cancel', 'cancelled', 'complaint', 'issue', 
        'problem', 'error', 'broken', 'not working', 'failed'
    ]
    
    low_priority_keywords = [
        'question', 'inquiry', 'info', 'information', 'general',
        'feedback', 'suggestion'
    ]
    
    combined_text = (subject + " " + email_text).lower()
    
    for keyword in high_priority_keywords:
        if keyword in combined_text:
            return "HIGH"
    
    for keyword in low_priority_keywords:
        if keyword in combined_text and not any(hp in combined_text for hp in high_priority_keywords):
            return "LOW"
    
    return "MEDIUM"


def _is_complaint_or_error(email_text: str, subject: str = "") -> bool:
    """Check if email appears to be a complaint, error, or issue that needs attention."""
    complaint_keywords = [
        'complaint', 'complain', 'issue', 'problem', 'error', 'bug', 'broken',
        'not working', 'failed', 'failure', 'refund', 'cancel', 'cancelled',
        'disappointed', 'unhappy', 'unsatisfied', 'wrong', 'incorrect',
        'fix', 'repair', 'resolve', 'help', 'support', 'assistance'
    ]
    
    combined_text = (subject + " " + email_text).lower()
    
    # Check if email contains complaint/error keywords
    for keyword in complaint_keywords:
        if keyword in combined_text:
            return True
    
    # Check if issue description is substantial (more than just greetings)
    issue_desc = _extract_issue_description(email_text)
    if len(issue_desc.strip()) > 50:  # Has substantial content
        return True
    
    return False


def _has_required_information(payload: Dict[str, Any]) -> tuple:
    """Check if payload has required information for processing."""
    missing = []
    
    # Check if customer email is valid (not default)
    if not payload.get("CustomerEmail") or payload.get("CustomerEmail") == "unknown@example.com":
        missing.append("CustomerEmail")
    
    # Check if customer name is valid (not default)
    if not payload.get("CustomerName") or payload.get("CustomerName") == "Unknown":
        missing.append("CustomerName")
    
    # Check if issue description is substantial
    issue_desc = payload.get("IssueDescription", "").strip()
    if len(issue_desc) < 20:  # Too short to be meaningful
        missing.append("IssueDescription")
    
    return len(missing) == 0, missing


def _save_payload_to_file(payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> str:
    """Save payload to JSON file when webhook is not available."""
    try:
        # Load existing payloads
        if os.path.exists(PAYLOADS_FILE):
            with open(PAYLOADS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"payloads": []}
        
        # Add new payload with timestamp
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "payload": payload,
            "metadata": metadata or {}
        }
        data["payloads"].append(entry)
        
        # Save back to file
        with open(PAYLOADS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return PAYLOADS_FILE
    except Exception as e:
        print(f"Error saving payload to file: {e}")
        return ""


def _get_gmail_access_token() -> Optional[str]:
    """Get Gmail API access token, refreshing if needed."""
    if GMAIL_ACCESS_TOKEN:
        return GMAIL_ACCESS_TOKEN
    
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
                return data.get('access_token')
        except Exception as e:
            print(f"Error refreshing token: {e}")
    
    return None


def _send_reply_email(to_email: str, subject: str, body: str, reply_to_message_id: Optional[str] = None) -> Dict[str, Any]:
    """Send a reply email using Gmail API."""
    token = _get_gmail_access_token()
    if not token:
        return {
            "status": "error",
            "error": "Gmail access token not available. Cannot send reply email."
        }
    
    try:
        # Create email message
        message = MIMEText(body)
        message['To'] = to_email
        message['From'] = GMAIL_REPLY_EMAIL
        message['Subject'] = subject
        
        # Add In-Reply-To and References headers if replying to a message
        if reply_to_message_id:
            message['In-Reply-To'] = reply_to_message_id
            message['References'] = reply_to_message_id
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Send via Gmail API
        url = f"{GMAIL_API_BASE}/users/me/messages/send"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = {
            'raw': raw_message
        }
        
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return {
                "status": "success",
                "message": "Reply email sent successfully",
                "message_id": response.json().get('id')
            }
        else:
            return {
                "status": "error",
                "error": f"Failed to send reply email. HTTP {response.status_code}",
                "response": response.text
            }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to send reply email: {str(e)}"
        }


@tool
def process_email(
    email_text: str,
    from_header: Optional[str] = None,
    subject: Optional[str] = None,
    to_header: Optional[str] = None,
    date_header: Optional[str] = None,
    message_id: Optional[str] = None,
    thread_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Process an email to extract customer information and create a structured payload.
    
    Extracts:
    - CustomerName: from email signature, "I am" statements, or From header
    - CustomerEmail: from email content or From header
    - CustomerPhoneNumber: from email content
    - IssueDescription: main body content with greetings/signatures removed
    - Priority: based on keywords (HIGH/MEDIUM/LOW)
    - Subject: email subject line
    - EmailMetadata: additional email details (From, To, Subject, dates, etc.)
    
    Args:
        email_text: The email body text
        from_header: The "From" header (e.g., "John Doe <john@example.com>")
        subject: The email subject line
        to_header: The "To" header
        date_header: The "Date" header (optional)
        message_id: Gmail message ID (optional)
        thread_id: Gmail thread ID (optional)
    
    Returns a dict with the structured payload ready to send to another agent.
    """
    
    # Extract customer email
    customer_email = None
    if from_header:
        name, email = parseaddr(from_header)
        if email:
            customer_email = email
    if not customer_email:
        customer_email = _extract_email_address(email_text)
    
    # Extract customer name
    customer_name = _extract_name(email_text, from_header or "")
    
    # Extract phone number
    customer_phone = _extract_phone_number(email_text)
    
    # Extract issue description (include subject if relevant)
    issue_description = _extract_issue_description(email_text)
    # If subject contains important info, prepend it to issue description
    if subject and subject.strip():
        subject_lower = subject.lower()
        # Check if subject contains complaint/issue keywords
        if any(kw in subject_lower for kw in ['urgent', 'complaint', 'issue', 'problem', 'refund', 'cancel', 'error']):
            issue_description = f"[Subject: {subject}] {issue_description}"
    
    # Determine priority (subject is already considered in the function)
    priority = _determine_priority(email_text, subject or "")
    
    # Create payload in the required format with enhanced details
    payload = {
        "CustomerName": customer_name or "Unknown",
        "CustomerEmail": customer_email or "unknown@example.com",
        "CustomerPhoneNumber": customer_phone or "",
        "IssueDescription": issue_description,
        "Priority": priority,
        "Subject": subject or "",
        "EmailMetadata": {
            "From": from_header or "",
            "To": to_header or "",
            "Subject": subject or "",
            "Date": date_header or "",
            "MessageID": message_id or "",
            "ThreadID": thread_id or "",
            "HasSubject": bool(subject and subject.strip()),
            "SubjectLength": len(subject or ""),
            "BodyLength": len(email_text or "")
        }
    }
    
    return {
        "status": "success",
        "payload": payload,
        "extracted_info": {
            "name_found": customer_name is not None,
            "email_found": customer_email is not None,
            "phone_found": customer_phone is not None,
            "subject_found": bool(subject and subject.strip())
        }
    }


@tool
def send_to_agent(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send the processed email payload to another agent for further processing.
    
    The payload should be in the format:
    {
        "CustomerName": "...",
        "CustomerEmail": "...",
        "CustomerPhoneNumber": "...",
        "IssueDescription": "...",
        "Priority": "HIGH|MEDIUM|LOW"
    }
    
    This can send to:
    1. A webhook URL (if AGENT_WEBHOOK_URL is set)
    2. Another orchestrate agent via collaboration (if configured)
    3. An API endpoint
    
    Returns status of the send operation.
    """
    
    if not isinstance(payload, dict):
        return {"status": "error", "error": "Payload must be a dictionary"}
    
    # Validate required fields
    required_fields = ["CustomerName", "CustomerEmail", "IssueDescription", "Priority"]
    missing_fields = [field for field in required_fields if not payload.get(field)]
    if missing_fields:
        return {"status": "error", "error": f"Missing required fields: {', '.join(missing_fields)}"}
    
    # Determine which webhook URL to use based on environment
    webhook_url = AGENT_WEBHOOK_URL
    if not webhook_url:
        if ENVIRONMENT == 'production' and AGENT_WEBHOOK_URL_PRODUCTION:
            webhook_url = AGENT_WEBHOOK_URL_PRODUCTION
        elif ENVIRONMENT == 'local' and AGENT_WEBHOOK_URL_LOCAL:
            webhook_url = AGENT_WEBHOOK_URL_LOCAL
    
    # If webhook URL is configured, send via HTTP POST
    if webhook_url:
        try:
            headers = {"Content-Type": "application/json"}
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if 200 <= response.status_code < 300:
                return {
                    "status": "success",
                    "message": "Payload sent successfully to agent",
                    "status_code": response.status_code,
                    "response": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text
                }
            else:
                return {
                    "status": "error",
                    "error": f"Failed to send payload. HTTP {response.status_code}",
                    "status_code": response.status_code,
                    "response": response.text
                }
        except requests.RequestException as e:
            return {
                "status": "error",
                "error": f"Failed to send payload: {str(e)}"
            }
    
    # If no webhook configured, save to file
    saved_file = _save_payload_to_file(payload, {"saved_at": datetime.datetime.now().isoformat()})
    
    return {
        "status": "success",
        "message": "Payload prepared but no webhook configured. Payload saved to file.",
        "payload": payload,
        "saved_to_file": saved_file
    }


@tool
def process_and_send_email(
    email_text: str,
    from_header: Optional[str] = None,
    subject: Optional[str] = None,
    to_header: Optional[str] = None,
    date_header: Optional[str] = None,
    original_message_id: Optional[str] = None,
    thread_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Process an email and automatically send the extracted payload to another agent.
    
    This function:
    1. Processes the email to extract customer information
    2. Validates if it's a complaint/error and has required information
    3. If valid: sends to agent webhook or saves to file
    4. If invalid or missing info: sends reply email requesting more details
    
    Returns the result of processing and sending operations.
    """
    
    # Process the email
    process_result = process_email(
        email_text=email_text,
        from_header=from_header,
        subject=subject,
        to_header=to_header,
        date_header=date_header,
        message_id=original_message_id,
        thread_id=thread_id
    )
    
    if process_result.get("status") != "success":
        return process_result
    
    # Extract the payload
    payload = process_result.get("payload")
    if not payload:
        return {"status": "error", "error": "Failed to extract payload from email"}
    
    # Validate if email is a complaint/error
    is_complaint = _is_complaint_or_error(email_text, subject or "")
    
    # Check if required information is present
    has_required_info, missing_fields = _has_required_information(payload)
    
    # If not a complaint/error or missing required info, send reply email
    if not is_complaint or not has_required_info:
        customer_email = payload.get("CustomerEmail", "")
        customer_name = payload.get("CustomerName", "Valued Customer")
        
        # Don't send reply if email is invalid
        if not customer_email or customer_email == "unknown@example.com":
            return {
                "status": "error",
                "error": "Cannot send reply: invalid customer email address",
                "payload": payload,
                "validation": {
                    "is_complaint": is_complaint,
                    "has_required_info": has_required_info,
                    "missing_fields": missing_fields
                }
            }
        
        # Create reply message
        reply_subject = f"Re: {subject or 'Your inquiry'}"
        reply_body = f"""Dear {customer_name},

Thank you for contacting us.

We have received your email, but we need more information to assist you better. 

"""
        
        if not is_complaint:
            reply_body += """Your email does not appear to be a complaint or support request. 
If you have a specific issue, complaint, or need assistance, please provide:
- A detailed description of your issue or concern
- Any relevant booking or transaction details
- Any error messages you may have encountered

"""
        
        if not has_required_info:
            reply_body += f"""We are missing the following information:
- {', '.join(missing_fields)}

"""
        
        reply_body += """Please reply to this email with the additional details, and we will be happy to assist you.

Best regards,
Sherlox Support Team
"""
        
        # Send reply email
        reply_result = _send_reply_email(
            to_email=customer_email,
            subject=reply_subject,
            body=reply_body,
            reply_to_message_id=original_message_id
        )
        
        return {
            "status": "reply_sent",
            "message": "Reply email sent requesting more information",
            "processing": process_result,
            "reply": reply_result,
            "validation": {
                "is_complaint": is_complaint,
                "has_required_info": has_required_info,
                "missing_fields": missing_fields
            },
            "payload": payload
        }
    
    # If valid complaint/error with required info, send to agent
    send_result = send_to_agent(payload)
    
    return {
        "status": "success" if send_result.get("status") == "success" else "partial",
        "processing": process_result,
        "sending": send_result,
        "payload": payload,
        "validation": {
            "is_complaint": is_complaint,
            "has_required_info": has_required_info,
            "missing_fields": []
        }
    }

