# How to Perform a Local Run for the Project

This guide will walk you through setting up and running the Email Processor Agent locally on your machine.

## Prerequisites

- Python 3.11, 3.12, or 3.13 installed
- Google Cloud Console account
- Gmail account access for `reachus.sherlox@gmail.com`
- Internet connection for Gmail API access

## Step 1: Install Dependencies

Navigate to the `email_processor` directory and install required packages:

```bash
cd email_processor
pip install -r requirements.txt
```

Required packages include:
- `ibm-watsonx-orchestrate`
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`
- `requests`

## Step 2: Set Up Gmail API Authentication

### 2.1: Enable Gmail API in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing project
3. Navigate to **APIs & Services** → **Library**
4. Search for "Gmail API" and click **Enable**

### 2.2: Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. Choose application type: **Desktop app** (for local development)
4. Download the credentials JSON file
5. Save it as `credentials.json` in the `email_processor` directory

### 2.3: Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Fill in the required information:
   - User Type: External (for testing) or Internal (for organization)
   - App name, User support email, Developer contact information
3. Add scopes: `https://www.googleapis.com/auth/gmail.readonly` and `https://www.googleapis.com/auth/gmail.send`
4. Add test users (if in testing mode): Add `reachus.sherlox@gmail.com`

### 2.4: Run Authentication Script

Run the setup script to authenticate and get tokens:

```bash
python setup_gmail_auth.py
```

This script will:
- Open a browser window for Google authentication
- Ask you to sign in with the Gmail account (`reachus.sherlox@gmail.com`)
- Grant permissions to the application
- Generate and display access token and refresh token

**Save the tokens** - you'll need them for environment variables.

## Step 3: Configure Environment Variables

Set the following environment variables before running the application:

### Required Variables

```bash
# Gmail account to monitor
export GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"

# Option 1: Direct Access Token (simpler, expires in ~1 hour)
export GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."

# Option 2: OAuth2 Refresh Token (recommended for production)
export GMAIL_REFRESH_TOKEN="1//0g..."
export GMAIL_CLIENT_ID="123456789-abc.apps.googleusercontent.com"
export GMAIL_CLIENT_SECRET="GOCSPX-abc..."
```

### Optional Variables

```bash
# Webhook URL to send processed emails to another agent
export AGENT_WEBHOOK_URL="https://your-webhook-url.com/api/process"

# Email address to send replies from (default: same as GMAIL_WATCH_EMAIL)
export GMAIL_REPLY_EMAIL="reachus.sherlox@gmail.com"

# Polling interval in seconds (default: 60)
export GMAIL_POLL_INTERVAL="60"
```

### Setting Environment Variables

**On Windows (PowerShell):**
```powershell
$env:GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
$env:GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."
```

**On Windows (Command Prompt):**
```cmd
set GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
set GMAIL_ACCESS_TOKEN=ya29.a0AfH6SMBx...
```

**On Linux/Mac:**
```bash
export GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
export GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."
```

**Using .env file (recommended):**
Create a `.env` file in the `email_processor` directory:
```
GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
GMAIL_ACCESS_TOKEN=ya29.a0AfH6SMBx...
AGENT_WEBHOOK_URL=https://your-webhook-url.com/api/process
GMAIL_POLL_INTERVAL=60
```

Then load it using a tool like `python-dotenv` or manually source it.

## Step 4: Run the Gmail Watcher

The Gmail watcher continuously monitors the Gmail inbox for new emails and processes them automatically.

### Run the Watcher

```bash
python gmail_watcher.py
```

The watcher will:
- Poll Gmail API every 60 seconds (or your configured interval)
- Detect new unread emails sent to `reachus.sherlox@gmail.com`
- Process each email to extract customer information
- Send structured payloads to the configured webhook (or save to file)
- Mark emails as processed to avoid duplicates

### Expected Output

```
Starting Gmail watcher for reachus.sherlox@gmail.com
Found 2 new email(s) to process
Processing email: abc123...
Successfully processed email abc123
Sending payload to agent...
Payload sent successfully
```

## Step 5: Test the Agent Tools Locally

You can also test the agent tools directly without the watcher:

### Test Email Processing

Create a test script `test_local.py`:

```python
from email_processor import process_email

# Test email content
email_text = """
From: John Doe <john@example.com>
Subject: URGENT: Need refund for cancelled booking

Hello,
I am John Doe and I need an urgent refund for my cancelled booking.
My phone number is +1-555-123-4567.

Thanks,
John
"""

result = process_email(email_text)
print(json.dumps(result, indent=2))
```

Run it:
```bash
python test_local.py
```

### Test Sending to Agent

```python
from email_processor import process_and_send_email

email_text = """
From: Jane Smith <jane@example.com>
Subject: Complaint about service

I have an issue with my booking...
"""

result = process_and_send_email(email_text)
print(result)
```

## Step 6: Verify Local Setup

### Check Processed Emails

The system creates `processed_emails.json` to track processed emails:
```bash
cat processed_emails.json
```

### Check Saved Payloads

If no webhook is configured, payloads are saved to `saved_payloads.json`:
```bash
cat saved_payloads.json
```

### Send a Test Email

1. Send an email to `reachus.sherlox@gmail.com` from another account
2. Wait for the polling interval (default: 60 seconds)
3. Check the console output for processing logs
4. Verify the payload was created and sent

## Troubleshooting

### Authentication Errors

**Problem:** `401 Unauthorized` or token expired
- **Solution:** Access tokens expire after ~1 hour. Use refresh tokens instead or run `setup_gmail_auth.py` again

**Problem:** `403 Forbidden` - Insufficient permissions
- **Solution:** Check OAuth scopes include `gmail.readonly` and `gmail.send`

### Email Not Being Processed

**Problem:** No emails detected
- **Solution:** 
  - Verify `GMAIL_WATCH_EMAIL` matches the email address receiving emails
  - Check emails are unread (the watcher only processes unread emails)
  - Verify Gmail API is enabled in Google Cloud Console

**Problem:** Emails already processed
- **Solution:** Check `processed_emails.json` - emails are marked as processed to avoid duplicates

### Import Errors

**Problem:** Module not found errors
- **Solution:** Ensure you're in the `email_processor` directory and all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

### Network Errors

**Problem:** Cannot connect to Gmail API
- **Solution:** Check internet connection and firewall settings

## Next Steps

Once local setup is working:
- Test with various email formats
- Configure webhook URL to send to another agent
- Adjust polling interval based on email volume
- Set up monitoring and logging
- Proceed to deployment to IBM Watsonx Orchestrate

## Additional Resources

- Gmail API Documentation: https://developers.google.com/gmail/api
- Google OAuth 2.0 Guide: https://developers.google.com/identity/protocols/oauth2
- IBM Watsonx Orchestrate Documentation: https://www.ibm.com/docs/en/watsonx-orchestrate

