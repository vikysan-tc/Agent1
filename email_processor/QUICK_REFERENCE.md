# Email Processor - Quick Reference

## Environment Variables Summary

### Required
```bash
# Option 1: Direct Access Token (simpler, expires in 1 hour)
GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."

# Option 2: OAuth2 (recommended for production)
GMAIL_REFRESH_TOKEN="1//0g..."
GMAIL_CLIENT_ID="123456789-abc.apps.googleusercontent.com"
GMAIL_CLIENT_SECRET="GOCSPX-abc..."

# Gmail Configuration
GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
```

### Optional
```bash
AGENT_WEBHOOK_URL="https://your-webhook-url.com/api/process"
GMAIL_POLL_INTERVAL="60"  # seconds
```

## Quick Setup

### Local Development
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Setup Gmail auth**: `python setup_gmail_auth.py`
3. **Set environment variables** (see above)
4. **Run locally**: `python gmail_watcher.py`

### Deploy to Orchestrate
1. **Install dependencies**: `pip install -r requirements.txt`
2. **Setup Gmail auth**: `python setup_gmail_auth.py`
3. **Set environment variables** (see above)
4. **Deploy**: Upload `email_processor.yaml` and `email_processor.py`
5. **Run watcher** (optional): `python gmail_watcher.py`

## Processing Flow (Simplified)

```
Gmail Inbox → gmail_watcher.py (polls every 60s)
    ↓
Fetch Email Content
    ↓
email_processor.py → process_email()
    ↓
Extract: Name, Email, Phone, Issue, Priority
    ↓
Create Payload (JSON)
    ↓
send_to_agent() → POST to AGENT_WEBHOOK_URL
    ↓
Mark as Processed
```

## Output Payload Format

```json
{
    "CustomerName": "John Doe",
    "CustomerEmail": "john@example.com",
    "CustomerPhoneNumber": "+1-555-123-4567",
    "IssueDescription": "Need refund for cancelled booking",
    "Priority": "HIGH"
}
```

## Priority Levels

- **HIGH**: urgent, emergency, refund, cancel, complaint, problem, error
- **MEDIUM**: Default for most emails
- **LOW**: question, inquiry, feedback, suggestion

## Files

- `email_processor.py` - Main agent tools
- `gmail_watcher.py` - Standalone Gmail monitor
- `setup_gmail_auth.py` - Gmail API authentication setup
- `email_processor.yaml` - Agent configuration

## Documentation

- **Local Setup Guide**: [LOCAL_SETUP.md](LOCAL_SETUP.md) - Run locally and connect to Gmail
- **Full Environment Variables**: [ENV_VARIABLES.md](ENV_VARIABLES.md)
- **Detailed Processing Flow**: [PROCESSING_FLOW.md](PROCESSING_FLOW.md)
- **Deployment Guide**: [../DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md)

## Common Issues

| Issue | Solution |
|-------|----------|
| "Gmail access token not available" | Run `setup_gmail_auth.py` and set `GMAIL_ACCESS_TOKEN` |
| "Failed to refresh token" | Check OAuth2 credentials are correct |
| "Webhook URL not configured" | Set `AGENT_WEBHOOK_URL` or process manually |
| Emails not being processed | Check `GMAIL_WATCH_EMAIL` is correct |

## Tools Available

1. `process_email(email_text, from_header, subject, to_header)` - Extract info from email
2. `send_to_agent(payload)` - Send payload to webhook
3. `process_and_send_email(...)` - Do both in one call

