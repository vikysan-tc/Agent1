# CRM Integration Summary

This document summarizes the integration of the CRM backend API with the greeter agent and email processor.

## Changes Made

**Note: All greeter agent code is self-contained in the `greeter_agent` folder. No dependencies on `/tools` folder.**

### 1. Updated Greeter Tools to Use Local CRM Server

**Files Modified:**
- `greeter_agent/greeter_tools.py` (self-contained, all tools in this file)

**Changes:**
- Added support for `CRM_SERVER_URL` environment variable
- Defaults to `http://localhost:8080` for local development
- Can be overridden for production deployments

**Before:**
```python
TICKETS_URL = "https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver/api/tickets"
```

**After:**
```python
CRM_SERVER_URL = os.environ.get('CRM_SERVER_URL', 'http://localhost:8080')
TICKETS_URL = f"{CRM_SERVER_URL}/api/tickets"
```

### 2. Created CRM Email Response Generator

**New File:** `greeter_agent/crm_email_generator.py`

**Features:**
- Fetches ticket data from CRM API to enrich email content
- Fetches booking data from CRM API for booking-related emails
- Generates personalized email responses based on CRM data
- Functions:
  - `get_ticket_by_reference()` - Fetch ticket details
  - `get_bookings_by_email()` - Fetch customer bookings
  - `generate_ticket_created_email_body()` - Generate ticket creation email
  - `generate_booking_acknowledgement_email_body()` - Generate booking acknowledgement email
  - `generate_refund_reinitiated_email_body()` - Generate refund reinitiation email
  - `generate_mock_email_response()` - Unified mock response generator

### 3. Enhanced Email Sender with CRM Integration

**File Modified:** `greeter_agent/email_sender.py`

**Changes:**
- Integrated CRM email generator for richer email content
- Falls back to basic email templates if CRM generator is unavailable
- Email functions now use CRM API data when available:
  - `send_ticket_created_email()` - Uses ticket data from CRM
  - `send_booking_acknowledgement_email()` - Uses booking data from CRM
  - `send_refund_reinitiated_email()` - Uses booking data from CRM

### 4. Created Combined Local Run Script

**New File:** `local_run_combined.ps1`

**Features:**
- Starts all services in separate PowerShell windows:
  - CRM Server (Spring Boot on port 8080)
  - Greeter Agent Server (Flask on port 5000)
  - Email Processor Watcher (Gmail API polling)
- Automatically sets environment variables
- Waits for services to be ready before starting next service
- Handles service dependencies
- Provides health checks and testing commands

**Usage:**
```powershell
.\local_run_combined.ps1 -GmailAccessToken "your-token" -OrchestrateUrl "https://..." -OrchestrateApiKey "your-key"
```

### 5. Created Comprehensive Documentation

**New File:** `LOCAL_RUN_COMBINED.md`

**Contents:**
- Prerequisites and setup instructions
- Quick start guide
- Manual setup steps
- Integration flow explanation
- API endpoints reference
- Testing instructions
- Troubleshooting guide
- Configuration options

## Integration Flow

```
Email Received (Gmail)
    ↓
Email Processor (extracts customer info)
    ↓
Greeter Agent Webhook (localhost:5000/webhook)
    ↓
Greeter Agent (creates ticket via CRM API)
    ↓
CRM Server (localhost:8080/api/tickets)
    ↓
CRM Email Generator (fetches ticket/booking data)
    ↓
Email Sender (sends enriched email to customer)
```

## Environment Variables

### Required for Local Run
- `CRM_SERVER_URL` - Default: `http://localhost:8080`
- `GMAIL_ACCESS_TOKEN` - Gmail API access token
- `GMAIL_WATCH_EMAIL` - Email to monitor (default: `reachus.sherlox@gmail.com`)
- `AGENT_WEBHOOK_URL` - Greeter agent webhook (default: `http://localhost:5000/webhook`)
- `ORCHESTRATE_URL` - IBM Watsonx Orchestrate instance URL
- `ORCHESTRATE_API_KEY` - IBM Watsonx Orchestrate API key

### Optional
- `GMAIL_REFRESH_TOKEN` - For token refresh
- `GMAIL_CLIENT_ID` - OAuth2 client ID
- `GMAIL_CLIENT_SECRET` - OAuth2 client secret
- `GMAIL_POLL_INTERVAL` - Email polling interval in seconds (default: 60)
- `ENVIRONMENT` - Environment setting (default: `local`)

## Benefits

1. **Unified Local Development**: All services can be started with a single command
2. **CRM Integration**: Email responses are enriched with actual CRM data
3. **Mock Responses**: CRM API data is used to generate realistic email responses
4. **Easy Testing**: Complete integration flow can be tested locally
5. **Flexible Configuration**: Environment variables allow easy switching between local and production

## Testing

### Test CRM Server
```powershell
Invoke-WebRequest http://localhost:8080/api/tickets
```

### Test Greeter Agent
```powershell
Invoke-WebRequest http://localhost:5000/health
```

### Test Integration
Send a test email to `reachus.sherlox@gmail.com` and verify:
1. Email is processed by email processor
2. Payload is sent to greeter agent
3. Ticket is created in CRM
4. Customer receives email notification with CRM data

## Next Steps

1. Test the complete integration flow
2. Verify email responses include CRM data
3. Test booking acknowledgement workflow
4. Test UPI collection workflow
5. Configure production environment variables
6. Deploy to production environments
