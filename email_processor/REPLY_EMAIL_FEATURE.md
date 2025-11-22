# Reply Email Feature

## Overview

The Email Processor Agent can automatically send reply emails to customers when:
1. The email doesn't appear to be a complaint or error
2. Required information is missing from the email

## Configuration

### Environment Variable

```bash
GMAIL_REPLY_EMAIL="reachus.sherlox@gmail.com"
```

- **Default**: `reachus.sherlox@gmail.com`
- **Required**: No (only needed if you want reply functionality)
- **Note**: The authenticated Gmail account must have permission to send from this address

### Gmail API Permissions

To send emails, you need Gmail API scopes that include sending:
- `https://www.googleapis.com/auth/gmail.send` (minimum)
- OR `https://www.googleapis.com/auth/gmail.modify` (includes send)

Update `setup_gmail_auth.py` to include the send scope:

```python
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send'  # Add this for sending emails
]
```

## When Reply Emails Are Sent

### 1. Email Not a Complaint/Error

The system checks if the email contains complaint/error keywords:
- `complaint`, `issue`, `problem`, `error`, `refund`, `cancel`, etc.
- If none found AND issue description is too short (<50 chars), reply is sent

### 2. Missing Required Information

The system validates:
- **Customer Email**: Must be valid (not "unknown@example.com")
- **Customer Name**: Must be valid (not "Unknown")
- **Issue Description**: Must be substantial (>20 characters)

If any are missing, a reply is sent requesting the missing information.

## Reply Email Content

### Subject Line
```
Re: [Original Subject]
```

### Email Body Template

```
Dear [Customer Name],

Thank you for contacting us.

We have received your email, but we need more information to assist you better. 

[If not a complaint:]
Your email does not appear to be a complaint or support request. 
If you have a specific issue, complaint, or need assistance, please provide:
- A detailed description of your issue or concern
- Any relevant booking or transaction details
- Any error messages you may have encountered

[If missing information:]
We are missing the following information:
- [List of missing fields]

Please reply to this email with the additional details, and we will be happy to assist you.

Best regards,
Sherlox Support Team
```

## Processing Flow with Replies

```
Email Received
    ↓
Extract Information
    ↓
Validate: Is it a complaint/error?
    ↓
    ├─ NO → Send Reply Email → Mark as Processed
    │
    └─ YES → Check Required Information
            ↓
            ├─ Missing Info → Send Reply Email → Mark as Processed
            │
            └─ All Info Present → Send to Agent/Webhook → Mark as Processed
```

## Saved Payloads

When no webhook is configured, payloads are saved to:
- **File**: `saved_payloads.json`
- **Location**: `email_processor/saved_payloads.json`
- **Format**:
  ```json
  {
    "payloads": [
      {
        "timestamp": "2024-01-15T10:30:00",
        "payload": {
          "CustomerName": "...",
          "CustomerEmail": "...",
          ...
        },
        "metadata": {
          "saved_at": "2024-01-15T10:30:00"
        }
      }
    ]
  }
  ```

## Testing Reply Emails

### Test Case 1: Non-Complaint Email
Send an email with just a greeting:
```
Subject: Hello
Body: Hi, just wanted to say hello!
```

**Expected**: Reply email sent requesting more details.

### Test Case 2: Missing Information
Send an email without name:
```
Subject: Need help
Body: I have an issue with my booking.
```

**Expected**: Reply email sent requesting name and other missing info.

### Test Case 3: Valid Complaint
Send a complete complaint:
```
Subject: Refund Request
Body: Hi, I am John Doe. I need a refund for my cancelled booking. 
My email is john@example.com and phone is +1-555-1234.
```

**Expected**: Processed and sent to agent/webhook, no reply sent.

## Troubleshooting

### "Gmail access token not available. Cannot send reply email."
- **Cause**: Missing or invalid Gmail API credentials
- **Solution**: Set `GMAIL_ACCESS_TOKEN` or configure OAuth2 credentials

### "Cannot send reply: invalid customer email address"
- **Cause**: Customer email could not be extracted from email
- **Solution**: Email is still processed but no reply is sent

### Reply emails not being sent
- **Check**: `GMAIL_REPLY_EMAIL` is set correctly
- **Check**: Gmail API has `gmail.send` scope
- **Check**: Authenticated account can send from reply email address
- **Check**: Email validation logic (may be too strict/lenient)

## Customization

### Adjusting Complaint Detection

Edit `_is_complaint_or_error()` in `email_processor.py`:
```python
complaint_keywords = [
    'complaint', 'your-custom-keyword', ...
]
```

### Adjusting Required Information

Edit `_has_required_information()` in `email_processor.py`:
```python
# Change minimum issue description length
if len(issue_desc) < 20:  # Adjust this value
    missing.append("IssueDescription")
```

### Customizing Reply Email Template

Edit the reply body in `process_and_send_email()` function:
```python
reply_body = f"""Your custom email template here..."""
```

