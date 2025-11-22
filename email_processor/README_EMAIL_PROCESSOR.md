# Email Processor Agent for IBM Watsonx Orchestrate

This agent monitors Gmail for emails sent to `reachus.sherlox@gmail.com`, processes them to extract customer information and complaints, and sends structured payloads to another agent for further processing.

## Files

- `email_processor.py` - Main agent tools for processing emails
- `email_processor.yaml` - Agent configuration for IBM watsonx orchestrate
- `gmail_worker.py` - Background worker to poll Gmail and trigger processing
- `requirements_email.txt` - Python dependencies

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements_email.txt
```

### 2. Configure Environment Variables

Set the following environment variables:

```bash
# Gmail Configuration
export GMAIL_EMAIL="reachus.sherlox@gmail.com"
export GMAIL_PASSWORD="your-app-password"  # Use Gmail App Password, not regular password
export GMAIL_IMAP_SERVER="imap.gmail.com"

# Agent Configuration
export AGENT_WEBHOOK_URL="https://your-agent-webhook-url.com/api/process"
export ORCHESTRATE_AGENT_URL="https://your-orchestrate-agent-url.com"  # Optional: for triggering agent via API
```

**Important**: For Gmail, you need to:
1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the App Password (not your regular password) for `GMAIL_PASSWORD`

### 3. Deploy to IBM Watsonx Orchestrate

#### Option A: Deploy from Local Files

1. Ensure you have the IBM watsonx orchestrate CLI installed and configured
2. Deploy the agent:

```bash
# Deploy the agent
ibm-watsonx-orchestrate deploy email_processor.yaml --tools email_processor.py
```

#### Option B: Manual Deployment via UI

1. Log into IBM Watsonx Orchestrate
2. Create a new agent
3. Upload `email_processor.yaml` as the agent configuration
4. Upload `email_processor.py` as the tools file
5. Configure the agent with the required environment variables

### 4. Run the Background Worker (Optional)

The `gmail_worker.py` script continuously polls Gmail for new emails and triggers the agent:

```bash
python gmail_worker.py
```

Or run it as a background service:

```bash
# Linux/Mac
nohup python gmail_worker.py > gmail_worker.log 2>&1 &

# Windows (PowerShell)
Start-Process python -ArgumentList "gmail_worker.py" -WindowStyle Hidden
```

## Usage

### Automatic Processing (Recommended)

1. Deploy the agent to orchestrate
2. Run `gmail_worker.py` as a background service
3. The worker will automatically:
   - Poll Gmail every 60 seconds (configurable via `POLL_INTERVAL`)
   - Detect new emails sent to `reachus.sherlox@gmail.com`
   - Trigger the agent to process them
   - Send structured payloads to your configured agent webhook

### Manual Processing

You can also manually trigger email processing by calling the agent with:

```python
# Via agent API or chat interface
fetch_and_process_gmail_emails()
```

## Output Payload Format

The agent processes emails and creates payloads in this format:

```json
{
    "CustomerName": "Logan Paul",
    "CustomerEmail": "logan@example.com",
    "CustomerPhoneNumber": "555-1234",
    "IssueDescription": "Need refund for cancelled booking",
    "Priority": "HIGH"
}
```

### Priority Levels

- **HIGH**: Contains urgent keywords (urgent, refund, complaint, legal action, etc.)
- **MEDIUM**: Contains issue/problem keywords (issue, problem, help, support, etc.)
- **LOW**: General inquiries or other messages

## Email Processing Logic

The agent extracts:

1. **Customer Name**: From email headers, "I am <Name>", signature lines, or "My name is <Name>"
2. **Customer Email**: From email "From" header or first email found in body
3. **Customer Phone**: Phone numbers found in email body (various formats supported)
4. **Issue Description**: Email body with greetings, signatures, and contact info removed
5. **Priority**: Determined by analyzing complaint and urgency keywords

## Troubleshooting

### Gmail Connection Issues

- Ensure 2FA is enabled and you're using an App Password
- Check that IMAP is enabled in Gmail settings
- Verify firewall/network allows IMAP connections (port 993)

### Agent Not Processing Emails

- Check that `AGENT_WEBHOOK_URL` is correctly set
- Verify the agent is deployed and running
- Check agent logs for errors
- Ensure `processed_emails.json` is writable (prevents duplicate processing)

### Missing Customer Information

- The agent uses heuristics to extract information
- Some emails may not have all fields (name, phone) - these will be set to empty strings or "Unknown"
- Review the `process_email` tool logic to customize extraction patterns

## File Structure

```
.
├── email_processor.py          # Main agent tools
├── email_processor.yaml        # Agent configuration
├── gmail_worker.py             # Background worker
├── requirements_email.txt      # Dependencies
├── processed_emails.json       # Tracks processed emails (auto-created)
└── README_EMAIL_PROCESSOR.md   # This file
```

## Security Notes

- Never commit `processed_emails.json` or credentials to version control
- Use environment variables or secure secret management for passwords
- Consider using OAuth2 instead of App Passwords for production
- Regularly rotate Gmail App Passwords

## Next Steps

1. Configure the receiving agent's webhook URL
2. Test with a sample email sent to `reachus.sherlox@gmail.com`
3. Monitor the agent logs to ensure proper processing
4. Adjust priority keywords and extraction patterns as needed

