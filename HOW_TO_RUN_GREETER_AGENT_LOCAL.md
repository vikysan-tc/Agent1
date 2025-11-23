# How to Run Greeter Agent Locally and Connect Email Processor

This guide explains how to run the greeter agent locally and configure the email processor to send payloads to it.

## Quick Start

1. **Install dependencies:**
   ```bash
   cd greeter_agent
   pip install -r requirements.txt
   ```

2. **Set up Gmail authentication:**
   ```bash
   # Place credentials.json in greeter_agent directory (from Google Cloud Console)
   python setup_gmail_auth.py
   ```

3. **Set environment variables:**
   ```powershell
   # PowerShell
   $env:CRM_SERVER_URL="http://localhost:8080"
   $env:WEBHOOK_PORT="5000"
   ```

4. **Start the server:**
   ```bash
   python server.py
   ```

5. **Test the health endpoint:**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:5000/health"
   ```

## Overview

The integration flow:
```
Email Processor (gmail_watcher.py) → POST /webhook → Greeter Agent Server (server.py) → Ticket Creation & Email Notifications
```

**Note:** The greeter agent runs independently for local development. It directly uses tools defined in `greeter_tools.py` and doesn't require IBM Watsonx Orchestrate for local runs.

## What Does the Greeter Agent Do?

The greeter agent is a Flask web server that:

1. **Receives webhook requests** from the email processor with customer inquiry data
2. **Creates tickets** in the CRM system via API calls
3. **Sends email notifications** to customers confirming ticket creation
4. **Handles booking acknowledgements** for refund requests
5. **Manages UPI ID collection** for refund processing
6. **Sends follow-up emails** as needed

The agent processes JSON payloads containing:
- Customer name and email
- Issue description
- Priority level
- Phone number (optional)

## Prerequisites

- Python 3.11, 3.12, or 3.13
- Gmail API credentials (for sending email notifications)
- CRM Server (optional, for ticket creation - can run on localhost:8080)
- Google Cloud Console project with Gmail API enabled (for email notifications)

## Step 1: Install Dependencies

### Install Greeter Agent Dependencies

```bash
cd greeter_agent
pip install -r requirements.txt
```

**Required packages:**
- `flask` - Web server framework
- `requests` - HTTP client for CRM API calls
- `google-api-python-client` - Gmail API client
- `google-auth` - Google authentication
- `google-auth-oauthlib` - OAuth2 flow
- `google-auth-httplib2` - HTTP transport for auth

### Install Email Processor Dependencies

```bash
cd email_processor
pip install -r requirements.txt
```

## Step 2: Set Up Gmail Authentication

The greeter agent needs Gmail API credentials to send email notifications to customers.

### Option A: Using OAuth2 (Recommended for Local Development)

1. **Get Google Cloud Credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Gmail API:
     - Go to "APIs & Services" > "Library"
     - Search for "Gmail API" and click "Enable"
   - Create OAuth 2.0 credentials:
     - Go to "APIs & Services" > "Credentials"
     - Click "Create Credentials" > "OAuth client ID"
     - Choose "Desktop app" as the application type
     - Download the credentials JSON file

2. **Set Up Authentication:**
   ```bash
   cd greeter_agent
   # Place your downloaded credentials.json file in this directory
   python setup_gmail_auth.py
   ```
   
   This will:
   - Open a browser window for OAuth authorization
   - Save the token to `token.pickle` for future use
   - Display the access token (you can use this for environment variable)

### Option B: Using Access Token Directly

If you already have a Gmail access token, you can set it as an environment variable (see Step 3).

**Note:** Access tokens expire after ~1 hour. For production, use refresh tokens or OAuth2 flow.

## Step 3: Configure Environment Variables

### For Greeter Agent

Set these environment variables before starting the greeter agent server:

**Windows PowerShell:**
```powershell
# CRM Server (optional - defaults to http://localhost:8080)
$env:CRM_SERVER_URL="http://localhost:8080"

# Server Configuration
$env:WEBHOOK_PORT="5000"
$env:WEBHOOK_HOST="0.0.0.0"

# Gmail API (for email notifications)
# Option 1: Use access token (if you have one)
$env:GMAIL_ACCESS_TOKEN="your-gmail-access-token"
$env:GMAIL_SENDER_EMAIL="noreply-sherlox@gmail.com"

# Option 2: Use OAuth2 credentials (if using token.pickle)
# No environment variables needed - token.pickle will be used automatically
```

**Windows CMD:**
```cmd
set CRM_SERVER_URL=http://localhost:8080
set WEBHOOK_PORT=5000
set WEBHOOK_HOST=0.0.0.0
set GMAIL_ACCESS_TOKEN=your-gmail-access-token
set GMAIL_SENDER_EMAIL=noreply-sherlox@gmail.com
```

**Linux/Mac:**
```bash
export CRM_SERVER_URL="http://localhost:8080"
export WEBHOOK_PORT="5000"
export WEBHOOK_HOST="0.0.0.0"
export GMAIL_ACCESS_TOKEN="your-gmail-access-token"
export GMAIL_SENDER_EMAIL="noreply-sherlox@gmail.com"
```

**Important Notes:**
- If you set up OAuth2 using `setup_gmail_auth.py`, the `token.pickle` file will be used automatically - you don't need to set `GMAIL_ACCESS_TOKEN`
- If you're using an access token directly, set `GMAIL_ACCESS_TOKEN` (tokens expire after ~1 hour)
- `GMAIL_SENDER_EMAIL` defaults to `noreply-sherlox@gmail.com` if not set

### For Email Processor

Set these environment variables to connect to the greeter agent:

**Windows PowerShell:**
```powershell
$env:GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
$env:GMAIL_ACCESS_TOKEN="your-gmail-access-token"
$env:AGENT_WEBHOOK_URL="http://localhost:5000/webhook"
$env:ENVIRONMENT="local"
$env:GMAIL_POLL_INTERVAL="60"
```

**Windows CMD:**
```cmd
set GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
set GMAIL_ACCESS_TOKEN=your-gmail-access-token
set AGENT_WEBHOOK_URL=http://localhost:5000/webhook
set ENVIRONMENT=local
set GMAIL_POLL_INTERVAL=60
```

**Linux/Mac:**
```bash
export GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
export GMAIL_ACCESS_TOKEN="your-gmail-access-token"
export AGENT_WEBHOOK_URL="http://localhost:5000/webhook"
export ENVIRONMENT="local"
export GMAIL_POLL_INTERVAL="60"
```

**Important:** The `AGENT_WEBHOOK_URL` must point to `http://localhost:5000/webhook` (the greeter agent's webhook endpoint).

## Step 4: Start the Greeter Agent Server

1. Navigate to the greeter_agent directory:
```bash
cd greeter_agent
```

2. Start the server:
```bash
python server.py
```

You should see output like:
```
Starting Greeter Agent Server on 0.0.0.0:5000
Server is ready to receive webhook requests from email_processor
Ticket creation and email notifications will be handled automatically
```

**Note:** The greeter agent runs independently and doesn't require IBM Watsonx Orchestrate for local development. It directly uses the tools defined in `greeter_tools.py`.

### Available Endpoints

- **`GET /health`**: Health check endpoint
  - Returns: `{"status": "healthy", "service": "greeter_agent"}`

- **`POST /webhook`**: Main webhook endpoint for email processor
  - Accepts JSON payload with customer information
  - Creates ticket and sends email notification

- **`POST /chat`**: Direct chat endpoint for testing
  - Accepts JSON with `message` field
  - Can process ticket creation requests

3. Verify the server is running:
   - Open a new terminal
   - Test the health endpoint:
   
   **Windows PowerShell:**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:5000/health"
   ```
   
   **Linux/Mac:**
   ```bash
   curl http://localhost:5000/health
   ```

   You should get: `{"status": "healthy", "service": "greeter_agent"}`

## Step 5: Start the Email Processor

1. Open a **new terminal window** (keep the greeter agent server running)

2. Navigate to the email_processor directory:
```bash
cd email_processor
```

3. Make sure environment variables are set (especially `AGENT_WEBHOOK_URL`)

4. Start the Gmail watcher:
```bash
python gmail_watcher.py
```

You should see output like:
```
Starting Gmail watcher for reachus.sherlox@gmail.com
Polling interval: 60 seconds
```

## Step 6: Test the Integration

### Test 1: Direct Webhook Test

Test if the greeter agent is receiving webhooks correctly:

**Windows PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/webhook" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"CustomerName":"Test User","CustomerEmail":"test@example.com","IssueDescription":"Test issue","Priority":"HIGH"}'
```

**Linux/Mac:**
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{"CustomerName":"Test User","CustomerEmail":"test@example.com","IssueDescription":"Test issue","Priority":"HIGH"}'
```

**Expected Response:**
```json
{
  "status": "success",
  "result": {
    "ticket_id": "...",
    "ticket_reference": "...",
    "email_sent": true,
    ...
  }
}
```

If there's an error, you'll see:
```json
{
  "status": "error",
  "error": "Error message here"
}
```

**Common Issues:**
- If you see "Greeter tools not available", make sure `greeter_tools.py` is in the same directory as `server.py`
- If you see CRM API errors, verify the CRM server is running and `CRM_SERVER_URL` is correct
- If you see Gmail API errors, verify Gmail authentication is set up correctly

### Test 2: End-to-End Email Test

1. Send a test email to `reachus.sherlox@gmail.com` with:
   - Subject: "URGENT: Need help with booking cancellation"
   - Body: "Hello, I am John Doe and I need help with my cancelled booking. My email is john@example.com and phone is +1-555-123-4567."

2. Wait up to 60 seconds (polling interval)

3. Check the email processor terminal - you should see:
   ```
   Found 1 new email(s) to process
   Processing email: abc123...
   Successfully processed email abc123
   Sending payload to agent...
   Payload sent successfully
   ```

4. Check the greeter agent terminal - you should see:
   ```
   Received webhook payload: {
     "CustomerName": "John Doe",
     "CustomerEmail": "john@example.com",
     ...
   }
   Agent response: {...}
   ```

## Troubleshooting

### Greeter Agent Not Starting

**Problem:** Server fails to start or shows errors

**Solutions:**
1. Check Python version: `python --version` (should be 3.11+)
2. Verify dependencies are installed:
   ```bash
   cd greeter_agent
   pip install -r requirements.txt
   ```
3. Check if port 5000 is already in use:
   - **Windows:** `netstat -ano | findstr :5000`
   - **Linux/Mac:** `lsof -i :5000`
4. Verify `greeter_tools.py` exists in the same directory as `server.py`
5. Check server logs for specific error messages

### Email Processor Not Sending to Greeter Agent

**Problem:** Email processor processes emails but doesn't send to greeter agent

**Solutions:**
1. Verify `AGENT_WEBHOOK_URL` is set correctly:
   ```powershell
   # PowerShell
   $env:AGENT_WEBHOOK_URL
   ```
   Should be: `http://localhost:5000/webhook`

2. Check if greeter agent server is running:
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:5000/health"
   ```

3. Check email processor logs for errors

4. Verify the email was actually processed (check `processed_emails.json` in email_processor directory)

### Connection Refused Errors

**Problem:** `Connection refused` or `Cannot connect to localhost:5000`

**Solutions:**
1. Ensure greeter agent server is running
2. Check firewall settings
3. Verify `WEBHOOK_HOST` is set to `0.0.0.0` (not `127.0.0.1`)
4. Try accessing `http://127.0.0.1:5000/health` instead

### CRM API Errors

**Problem:** Greeter agent shows errors when calling CRM API

**Solutions:**
1. Verify CRM server is running (if using local server):
   ```powershell
   # Test CRM server
   Invoke-WebRequest -Uri "http://localhost:8080/api/tickets"
   ```
2. Check `CRM_SERVER_URL` environment variable is set correctly
3. Verify CRM server is accessible and responding
4. Check server logs for specific CRM API error messages

### Gmail API Errors (Email Notifications Not Sending)

**Problem:** Greeter agent can't send email notifications

**Solutions:**
1. **If using OAuth2 (token.pickle):**
   - Verify `credentials.json` exists in `greeter_agent` directory
   - Verify `token.pickle` exists and is valid
   - Re-run `setup_gmail_auth.py` if token expired:
     ```bash
     cd greeter_agent
     python setup_gmail_auth.py
     ```

2. **If using access token:**
   - Verify `GMAIL_ACCESS_TOKEN` is set and valid
   - Check if token expired (tokens expire after ~1 hour)
   - Get a new token by running `setup_gmail_auth.py`

3. **General checks:**
   - Verify Gmail API is enabled in Google Cloud Console
   - Check that OAuth2 credentials have `gmail.send` scope
   - Verify `GMAIL_SENDER_EMAIL` is set correctly
   - Check server logs for specific Gmail API error messages

## Configuration Summary

### Greeter Agent Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CRM_SERVER_URL` | CRM server URL for ticket creation | `http://localhost:8080` | No |
| `WEBHOOK_PORT` | Port for webhook server | `5000` | No |
| `WEBHOOK_HOST` | Host for webhook server | `0.0.0.0` | No |
| `GMAIL_ACCESS_TOKEN` | Gmail API access token for sending emails | - | No* |
| `GMAIL_SENDER_EMAIL` | Email address to send from | `noreply-sherlox@gmail.com` | No |

**Note:** `GMAIL_ACCESS_TOKEN` is not required if you're using OAuth2 authentication (via `token.pickle` file created by `setup_gmail_auth.py`). Either use OAuth2 or provide an access token.

### Email Processor Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GMAIL_WATCH_EMAIL` | Email address to monitor | `reachus.sherlox@gmail.com` | Yes |
| `GMAIL_ACCESS_TOKEN` | Gmail API access token | - | Yes |
| `AGENT_WEBHOOK_URL` | Greeter agent webhook URL | - | Yes (for integration) |
| `ENVIRONMENT` | Environment setting | `local` | No |
| `GMAIL_POLL_INTERVAL` | Polling interval in seconds | `60` | No |

## Quick Start Script (Windows PowerShell)

Save this as `start_greeter_local.ps1`:

```powershell
# Set Greeter Agent Environment Variables
$env:CRM_SERVER_URL="http://localhost:8080"
$env:WEBHOOK_PORT="5000"
$env:WEBHOOK_HOST="0.0.0.0"
# Optional: Set Gmail access token if not using OAuth2
# $env:GMAIL_ACCESS_TOKEN="your-gmail-token-here"
$env:GMAIL_SENDER_EMAIL="noreply-sherlox@gmail.com"

# Start Greeter Agent Server
Write-Host "Starting Greeter Agent Server..." -ForegroundColor Green
cd greeter_agent
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python server.py"
cd ..

# Wait a moment for server to start
Start-Sleep -Seconds 3

# Set Email Processor Environment Variables
$env:GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
$env:GMAIL_ACCESS_TOKEN="your-gmail-token-here"
$env:AGENT_WEBHOOK_URL="http://localhost:5000/webhook"
$env:ENVIRONMENT="local"

# Start Email Processor
Write-Host "Starting Email Processor..." -ForegroundColor Green
cd email_processor
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python gmail_watcher.py"
cd ..

Write-Host "Both services started in separate windows!" -ForegroundColor Green
Write-Host "Make sure you've set up Gmail authentication first (run setup_gmail_auth.py)" -ForegroundColor Yellow
```

## Next Steps

Once both services are running:

1. **Monitor Logs**: Watch both terminal windows for processing activity
2. **Test with Real Emails**: Send test emails to `reachus.sherlox@gmail.com`
3. **Check CRM Integration**: Verify tickets are created in CRM (if CRM server is running)
4. **Test Email Notifications**: Verify customers receive email notifications

## Additional Resources

- [Greeter Agent README](greeter_agent/README.md)
- [Email Processor Local Run Guide](email_processor/How%20to%20perform%20a%20local%20run%20for%20the%20project.md)
- [Integration Guide](email_processor/INTEGRATION_WITH_GREETER.md)
- [Combined Local Run Guide](LOCAL_RUN_COMBINED.md)

