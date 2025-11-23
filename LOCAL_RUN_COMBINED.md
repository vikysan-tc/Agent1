# Combined Local Run Guide

This guide explains how to run all components of the Agent1 project locally in an integrated setup.

## Overview

The combined local run setup includes:
1. **CRM Server** (Spring Boot) - Runs on port 8080
2. **Greeter Agent Server** (Flask) - Runs on port 5000
3. **Email Processor Watcher** (Python) - Monitors Gmail for new emails

## Prerequisites

### Required Software
- **Java 17+** - For CRM Server
- **Maven 3.6+** (or use Maven wrapper in CRM-Server)
- **Python 3.11+** - For Greeter Agent and Email Processor
- **PowerShell 5.1+** (Windows) or PowerShell Core (Linux/Mac)

### Required Credentials
- **Gmail API Credentials**:
  - `GMAIL_ACCESS_TOKEN` - Gmail API access token
  - `GMAIL_REFRESH_TOKEN` (optional) - For token refresh
  - `GMAIL_CLIENT_ID` (optional) - OAuth2 client ID
  - `GMAIL_CLIENT_SECRET` (optional) - OAuth2 client secret
- **IBM Watsonx Orchestrate Credentials** (for Greeter Agent):
  - `ORCHESTRATE_URL` - Your Orchestrate instance URL
  - `ORCHESTRATE_API_KEY` - Your API key

## Quick Start

### Option 1: Using the PowerShell Script (Recommended for Windows)

```powershell
# Basic usage
.\local_run_combined.ps1

# With Gmail credentials
.\local_run_combined.ps1 -GmailAccessToken "your-token"

# With all credentials
.\local_run_combined.ps1 `
    -GmailAccessToken "your-token" `
    -OrchestrateUrl "https://your-instance.cloud.ibm.com" `
    -OrchestrateApiKey "your-api-key"

# Skip specific services
.\local_run_combined.ps1 -SkipCrmServer
.\local_run_combined.ps1 -SkipGreeterAgent
.\local_run_combined.ps1 -SkipEmailProcessor

# Custom CRM server path
.\local_run_combined.ps1 -CrmServerPath "C:\path\to\CRM-Server\orchestrate"
```

### Option 2: Manual Setup

#### Step 1: Set Environment Variables

**Windows PowerShell:**
```powershell
$env:CRM_SERVER_URL = "http://localhost:8080"
$env:GMAIL_ACCESS_TOKEN = "your-token"
$env:GMAIL_WATCH_EMAIL = "reachus.sherlox@gmail.com"
$env:AGENT_WEBHOOK_URL = "http://localhost:5000/webhook"
$env:ENVIRONMENT = "local"
$env:ORCHESTRATE_URL = "https://your-instance.cloud.ibm.com"
$env:ORCHESTRATE_API_KEY = "your-api-key"
```

**Windows CMD:**
```cmd
set CRM_SERVER_URL=http://localhost:8080
set GMAIL_ACCESS_TOKEN=your-token
set GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
set AGENT_WEBHOOK_URL=http://localhost:5000/webhook
set ENVIRONMENT=local
set ORCHESTRATE_URL=https://your-instance.cloud.ibm.com
set ORCHESTRATE_API_KEY=your-api-key
```

**Linux/Mac:**
```bash
export CRM_SERVER_URL=http://localhost:8080
export GMAIL_ACCESS_TOKEN=your-token
export GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
export AGENT_WEBHOOK_URL=http://localhost:5000/webhook
export ENVIRONMENT=local
export ORCHESTRATE_URL=https://your-instance.cloud.ibm.com
export ORCHESTRATE_API_KEY=your-api-key
```

#### Step 2: Start CRM Server

```bash
cd C:\Users\ANIKET R SHANKAR\Desktop\lablab_ibm\CRM-Server\orchestrate

# Windows
.\mvnw.cmd spring-boot:run

# Linux/Mac
./mvnw spring-boot:run
```

Wait for the server to start (check http://localhost:8080/actuator/health)

#### Step 3: Start Greeter Agent Server

```bash
cd greeter_agent
pip install -r requirements.txt
python server.py
```

The server will start on http://localhost:5000

#### Step 4: Start Email Processor Watcher

```bash
cd email_processor
pip install -r requirements.txt
python gmail_watcher.py
```

The watcher will start polling Gmail every 60 seconds.

## Integration Flow

1. **Email Received**: Customer sends email to `reachus.sherlox@gmail.com`
2. **Email Processing**: Email processor extracts customer information
3. **Send to Greeter**: Processed payload sent to `http://localhost:5000/webhook`
4. **Ticket Creation**: Greeter agent creates ticket via CRM API (`http://localhost:8080/api/tickets`)
5. **Booking Check**: Greeter agent checks for pending bookings via CRM API
6. **Email Notification**: Customer receives email notification (if configured)

## API Endpoints

### CRM Server (localhost:8080)
- `GET /api/tickets` - Get all tickets
- `POST /api/tickets` - Create a ticket
- `GET /api/tickets/bookings?email={email}` - Get bookings by email
- `GET /actuator/health` - Health check

### Greeter Agent Server (localhost:5000)
- `POST /webhook` - Receive email processor payloads
- `POST /chat` - Direct chat endpoint for testing
- `GET /health` - Health check

## Testing the Integration

### 1. Test CRM Server
```powershell
# Create a test ticket
Invoke-WebRequest -Uri "http://localhost:8080/api/tickets" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"customerName":"Test User","customerEmail":"test@example.com","issueDescription":"Test issue","priority":"HIGH"}'

# Get all tickets
Invoke-WebRequest -Uri "http://localhost:8080/api/tickets"

# Get bookings
Invoke-WebRequest -Uri "http://localhost:8080/api/tickets/bookings?email=test@example.com"
```

### 2. Test Greeter Agent
```powershell
# Health check
Invoke-WebRequest -Uri "http://localhost:5000/health"

# Send test payload
Invoke-WebRequest -Uri "http://localhost:5000/webhook" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"CustomerName":"Test User","CustomerEmail":"test@example.com","IssueDescription":"Test issue","Priority":"HIGH"}'
```

### 3. Test Email Processor
Send a test email to `reachus.sherlox@gmail.com` with:
- Subject: "URGENT: Need help with booking cancellation"
- Body: "Hello, I am John Doe and I need help with my cancelled booking. My email is john@example.com and phone is +1-555-123-4567."

The email processor should:
1. Detect the email within 60 seconds
2. Extract customer information
3. Send payload to greeter agent
4. Greeter agent creates ticket via CRM API
5. Customer receives email notification

## Configuration

### CRM Server Configuration
- Port: 8080 (configurable in `CRM-Server/orchestrate/src/main/resources/application.yml`)
- Base URL: `http://localhost:8080`

### Greeter Agent Configuration
- Port: 5000 (configurable via `WEBHOOK_PORT` environment variable)
- CRM API URL: `http://localhost:8080` (configurable via `CRM_SERVER_URL`)

### Email Processor Configuration
- Polling Interval: 60 seconds (configurable via `GMAIL_POLL_INTERVAL`)
- Watch Email: `reachus.sherlox@gmail.com` (configurable via `GMAIL_WATCH_EMAIL`)
- Webhook URL: `http://localhost:5000/webhook` (configurable via `AGENT_WEBHOOK_URL`)

## Troubleshooting

### CRM Server Not Starting
- **Check Java version**: `java -version` (should be 17+)
- **Check port 8080**: Ensure no other service is using port 8080
- **Check Maven**: Ensure Maven is installed or use Maven wrapper
- **Check logs**: Look for errors in the CRM server window

### Greeter Agent Not Starting
- **Check Python version**: `python --version` (should be 3.11+)
- **Check dependencies**: Run `pip install -r requirements.txt` in `greeter_agent` directory
- **Check port 5000**: Ensure no other service is using port 5000
- **Check Orchestrate credentials**: Ensure `ORCHESTRATE_URL` and `ORCHESTRATE_API_KEY` are set
- **Check CRM server**: Ensure CRM server is running on port 8080

### Email Processor Not Working
- **Check Gmail credentials**: Ensure `GMAIL_ACCESS_TOKEN` is set and valid
- **Check Gmail API**: Verify Gmail API is enabled in Google Cloud Console
- **Check permissions**: Ensure OAuth scopes include `gmail.readonly` and `gmail.send`
- **Check webhook**: Ensure greeter agent is running on port 5000
- **Check logs**: Look for errors in the email processor window

### Integration Issues
- **Check CRM server**: Verify CRM server is accessible at `http://localhost:8080`
- **Check greeter agent**: Verify greeter agent is accessible at `http://localhost:5000`
- **Check webhook URL**: Ensure `AGENT_WEBHOOK_URL` is set to `http://localhost:5000/webhook`
- **Check environment variables**: Ensure all required environment variables are set
- **Check logs**: Review logs in all service windows for errors

## Mock Email Responses

The system includes a CRM-based email response generator (`greeter_agent/crm_email_generator.py`) that:
- Fetches ticket data from CRM API to enrich email content
- Fetches booking data from CRM API for booking-related emails
- Generates personalized email responses based on CRM data

This ensures email responses are consistent with the data stored in the CRM system.

## Next Steps

Once local setup is working:
1. Test with various email formats
2. Test booking acknowledgement workflow
3. Test UPI collection workflow
4. Configure production environment variables
5. Deploy to production environments

## Additional Resources

- [CRM Server README](../CRM-Server/README.md)
- [Email Processor Local Run Guide](email_processor/How%20to%20perform%20a%20local%20run%20for%20the%20project.md)
- [Greeter Agent Integration Guide](email_processor/INTEGRATION_WITH_GREETER.md)

