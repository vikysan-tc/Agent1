# Email Processor Agent for IBM Watsonx Orchestrate

This agent monitors Gmail for emails sent to `reachus.sherlox@gmail.com`, processes them to extract customer information and complaints, and sends structured payloads to another agent for further processing.

## 📚 Documentation

- **[Local Setup Guide](LOCAL_SETUP.md)** - How to run locally and connect to Gmail
- **[Environment Variables Guide](ENV_VARIABLES.md)** - Complete guide to all required environment variables
- **[Processing Flow Documentation](PROCESSING_FLOW.md)** - Detailed explanation of how email processing works
- **[Knowledge Base](KNOWLEDGE_BASE.md)** - Comprehensive examples of customer complaints (flights, hotels, bookings, etc.)
- **[Reply Email Feature](REPLY_EMAIL_FEATURE.md)** - How automatic reply emails work
- **[Deployment Checklist](../DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment instructions
- **[Email Processor README](README_EMAIL_PROCESSOR.md)** - Additional technical details

## Quick Start

### Local Development

```bash
cd email_processor
pip install -r requirements.txt
python setup_gmail_auth.py  # First time setup for Gmail API
# Configure environment variables (see ENV_VARIABLES.md)
python gmail_watcher.py  # Run locally to process emails
```

**See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed local setup instructions.**

### Deploy to IBM Watsonx Orchestrate

```bash
# Deploy email_processor.yaml and email_processor.py to IBM Watsonx Orchestrate
```

## Project Structure

```
email_processor/
├── email_processor.py          # Main agent tools
├── email_processor.yaml        # Agent configuration
├── gmail_watcher.py            # Gmail monitoring (standalone)
├── setup_gmail_auth.py         # Gmail API setup
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── README_EMAIL_PROCESSOR.md   # Additional technical docs
├── ENV_VARIABLES.md            # Environment variables guide
├── PROCESSING_FLOW.md          # Processing flow documentation
└── processed_emails.json       # Tracks processed emails (auto-created)
```

## Features

- **Gmail Integration**: Monitors `reachus.sherlox@gmail.com` for new emails
- **Email Processing**: Extracts customer name, email, phone, and issue description
- **Priority Detection**: Automatically determines priority (HIGH/MEDIUM/LOW)
- **Structured Output**: Creates payloads with comprehensive details:
  ```json
  {
      "CustomerName": "Logan Paul",
      "CustomerEmail": "logan@example.com",
      "CustomerPhoneNumber": "555-1234",
      "IssueDescription": "Need refund for cancelled booking",
      "Priority": "HIGH",
      "Subject": "URGENT: Refund Request",
      "EmailMetadata": {
          "From": "Logan Paul <logan@example.com>",
          "To": "reachus.sherlox@gmail.com",
          "Subject": "URGENT: Refund Request",
          "Date": "2024-03-15T10:30:00Z",
          "MessageID": "abc123",
          "ThreadID": "xyz789",
          "HasSubject": true,
          "SubjectLength": 22,
          "BodyLength": 150
      }
  }
  ```
- **Agent Integration**: Sends processed payloads to another agent via webhook
- **Automatic Polling**: Continuously monitors Gmail for new emails
- **Duplicate Prevention**: Tracks processed emails to avoid reprocessing
- **Automatic Replies**: Sends reply emails when information is missing or email is not a complaint
- **Payload Storage**: Saves payloads to file when webhook is not configured

## Environment Variables

**Required:**
- `GMAIL_WATCH_EMAIL` - Email address to monitor (default: `reachus.sherlox@gmail.com`)
- `GMAIL_ACCESS_TOKEN` OR OAuth2 credentials (`GMAIL_REFRESH_TOKEN`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`)

**Optional:**
- `AGENT_WEBHOOK_URL` - Webhook URL to send processed payloads
- `GMAIL_REPLY_EMAIL` - Email address to send replies from (default: `reachus.sherlox@gmail.com`)
- `GMAIL_POLL_INTERVAL` - Polling interval in seconds (default: 60)

**See [ENV_VARIABLES.md](ENV_VARIABLES.md) for complete details.**

## How Processing Works

1. **Email Detection**: `gmail_watcher.py` polls Gmail API every 60 seconds (configurable)
2. **Email Fetching**: Retrieves full email content from Gmail API (including headers)
3. **Information Extraction**: Extracts customer name, email, phone, issue description, and **Subject line**
4. **Metadata Extraction**: Captures email metadata (From, To, Date, MessageID, ThreadID)
5. **Subject Analysis**: Analyzes subject line for urgency, booking references, and issue type
6. **Validation**: Checks if email is a complaint/error and has required information
7. **Reply Logic**: If invalid or missing info, sends reply email requesting details
8. **Priority Determination**: Analyzes content and subject for urgency keywords
9. **Payload Creation**: Creates structured JSON payload with all extracted information
10. **Webhook Sending**: Sends payload to configured webhook URL (or saves to file)
11. **Tracking**: Marks email as processed to prevent duplicates

**See [PROCESSING_FLOW.md](PROCESSING_FLOW.md) for detailed explanation.**
**See [REPLY_EMAIL_FEATURE.md](REPLY_EMAIL_FEATURE.md) for reply email details.**
**See [KNOWLEDGE_BASE.md](KNOWLEDGE_BASE.md) for examples of various complaint types.**

## Requirements

- Python 3.13
- IBM Watsonx Orchestrate account
- Gmail API credentials
- Google Cloud Console project with Gmail API enabled

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Gmail API Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create/select a project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download `credentials.json` to this directory
6. Run: `python setup_gmail_auth.py`

### 3. Configure Environment Variables
Set the required environment variables (see [ENV_VARIABLES.md](ENV_VARIABLES.md)):
```bash
export GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
export GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."
export AGENT_WEBHOOK_URL="https://your-webhook-url.com/api/process"
```

### 4. Deploy to IBM Watsonx Orchestrate
1. Upload `email_processor.yaml` as agent configuration
2. Upload `email_processor.py` as tools file
3. Configure environment variables in Orchestrate

### 5. Run Gmail Watcher (Optional)
For standalone monitoring:
```bash
python gmail_watcher.py
```

## Tools

The agent provides three tools:

1. **`process_email`**: Extracts customer information from email text
2. **`send_to_agent`**: Sends processed payload to webhook/agent
3. **`process_and_send_email`**: Combines both operations

## Support

For issues or questions:
1. Check [ENV_VARIABLES.md](ENV_VARIABLES.md) for configuration issues
2. Review [PROCESSING_FLOW.md](PROCESSING_FLOW.md) to understand the flow
3. See [DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md) for troubleshooting
4. Check IBM Watsonx Orchestrate documentation
5. Review Gmail API documentation

