# greetings.py
from ibm_watsonx_orchestrate.agent_builder.tools import tool
import requests
import json
import re
from typing import Optional, Dict, Any


@tool
def greeting() -> str:
    """Return a simple greeting string."""

    return "Hello World"


@tool
def create_ticket(
    customerName: str,
    customerEmail: str,
    issueDescription: str,
    customerPhone: Optional[str] = None,
    customerId: Optional[str] = None,
    priority: str = "HIGH",
) -> Dict[str, Any]:
    """
    Create a ticket by POSTing JSON to the ticket API.

    Mirrors the curl:
    curl -i -X POST "https://restaurants-cases-acceptance-volunteers.trycloudflare.com/api/tickets" -H "Content-Type: application/json" -d '{...}'

    Returns a dict with either {status: 'success', status_code, body}
    or {status: 'error', error, response_text}.
    """

    # Use the exact endpoint and JSON body as your curl example.
    url = "https://restaurants-cases-acceptance-volunteers.trycloudflare.com/api/tickets"
    payload = {
        "customerName": customerName,
        "customerEmail": customerEmail,
        "issueDescription": issueDescription,
        "customerPhone": customerPhone,
        "customerId": customerId,
        "priority": priority,
    }

    # Build raw JSON body (curl uses -d with raw JSON) and set Content-Type header
    body_str = json.dumps(payload)
    headers = {"Content-Type": "application/json"}

    try:
        # send the JSON as raw data to match curl behavior closely
        resp = requests.post(url, data=body_str, headers=headers, timeout=10)
        # include response headers and body for debugging
        result = {
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
        }

        try:
            result["body"] = resp.json()
        except ValueError:
            result["body"] = resp.text

        if 200 <= resp.status_code < 300:
            return {"status": "success", **result}
        else:
            # Non-2xx, return structured error info so the caller can see details
            return {"status": "error", "error": f"HTTP {resp.status_code}", **result}

    except requests.RequestException as e:
        # Capture as much info as possible for debugging
        resp_text = None
        status_code = None
        hdrs = None
        if getattr(e, "response", None) is not None:
            try:
                status_code = e.response.status_code
            except Exception:
                status_code = None
            try:
                resp_text = e.response.text
            except Exception:
                resp_text = None
            try:
                hdrs = dict(e.response.headers)
            except Exception:
                hdrs = None

        return {
            "status": "error",
            "error": str(e),
            "status_code": status_code,
            "response_text": resp_text,
            "response_headers": hdrs,
        }


@tool
def create_ticket_from_email(
    email_text: str,
    customerName: Optional[str] = None,
    customerEmail: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Extract customer name, email, phone and an issue description from a free-form email
    text and create a ticket by calling `create_ticket`.

    The function uses simple heuristics:
    - extracts the first email address found (if `customerEmail` not provided)
    - extracts a phone number-like token if present
    - looks for "I am <Name>" or "I'm <Name>" or a signature line (Regards/Best) for name
    - removes greeting/signature lines and lines containing email/phone to build the issueDescription

    Returns whatever `create_ticket` returns (status + details).
    """

    # find emails and phones inside the text
    found_emails = re.findall(r'[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}', email_text)
    found_phones = re.findall(r'\+?\d[\d\s\-\(\)]{6,}\d', email_text)

    # determine customerEmail and customerPhone
    email_val = customerEmail or (found_emails[0] if found_emails else None)
    phone_val = found_phones[0] if found_phones else None

    # try to extract name from explicit patterns
    name_val = customerName
    if not name_val:
        m = re.search(r"\bI(?:'m| am) ([A-Z][A-Za-z\s'`\-\.]{1,60})", email_text)
        if m:
            name_val = m.group(1).strip()
    # fallback: look for signature lines like 'Regards,\nName' or 'Best,\nName'
    if not name_val:
        sig = re.search(r'(?:Regards|Best|Thanks|Sincerely)[\,\s]*\n\s*([A-Z][A-Za-z\s\-\.]{1,60})', email_text, re.IGNORECASE)
        if sig:
            name_val = sig.group(1).strip()

    # build issueDescription by removing greeting/signature and lines with email/phone
    lines = [l.strip() for l in email_text.splitlines()]
    body_lines = []
    for ln in lines:
        if not ln:
            continue
        # skip common greetings
        if re.match(r'^(hi|hello|dear)\b', ln, re.IGNORECASE):
            continue
        # skip lines that are just the name or signature markers
        if re.match(r'^(regards|best|thanks|sincerely)\b', ln, re.IGNORECASE):
            break
        # skip lines that contain an email or phone
        if re.search(r'[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}', ln):
            continue
        if re.search(r'\+?\d[\d\s\-\(\)]{6,}\d', ln):
            continue
        # skip obvious name intro lines
        if re.match(r"^I(?:'m| am) ", ln, re.IGNORECASE):
            continue
        body_lines.append(ln)

    issue_description = ' '.join(body_lines).strip()
    if not issue_description:
        # fallback to whole text if our heuristic removed too much
        issue_description = email_text.strip()

    # ensure we have at least empty strings rather than None when calling create_ticket
    call_name = name_val or ""
    call_email = email_val or ""

    # call the existing create_ticket tool function (same module)
    try:
        result = create_ticket(
            customerName=call_name,
            customerEmail=call_email,
            issueDescription=issue_description,
            customerPhone=phone_val,
            customerId=None,
            priority="HIGH",
        )
        return result
    except Exception as e:
        return {"status": "error", "error": str(e)}


@tool
def create_ticket_from_json(payload: dict) -> Dict[str, Any]:
    """
    Accept a simple JSON/dict payload with keys:
      - CustomerName
      - CustomerEmail
      - CustomerPhoneNumber (optional)
      - IssueDescription
      - Priority (optional, defaults to 'HIGH')

    This function maps those keys to the existing `create_ticket` tool and returns its result.
    It accepts keys in several common casings (CustomerName, customerName, customer_name).
    """

    def _get(d, *keys):
        for k in keys:
            if k in d and d[k] is not None:
                return d[k]
        return None

    # If payload is a JSON string, try to parse it.
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception as e:
            return {"status": "error", "error": f"Invalid JSON payload: {e}"}

    if not isinstance(payload, dict):
        return {"status": "error", "error": "Payload must be a JSON object/dict"}

    customerName = _get(payload, 'CustomerName', 'customerName', 'customer_name') or ''
    customerEmail = _get(payload, 'CustomerEmail', 'customerEmail', 'customer_email') or ''
    customerPhone = _get(payload, 'CustomerPhoneNumber', 'customerPhoneNumber', 'customerPhone', 'customer_phone') or None
    issueDescription = _get(payload, 'IssueDescription', 'issueDescription', 'issue_description') or ''
    priority = _get(payload, 'Priority', 'priority') or 'HIGH'

    try:
        return create_ticket(
            customerName=customerName,
            customerEmail=customerEmail,
            issueDescription=issueDescription,
            customerPhone=customerPhone,
            customerId=None,
            priority=priority,
        )
    except Exception as e:
        return {"status": "error", "error": str(e)}