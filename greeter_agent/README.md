# Greeter Agent

An AI agent built with IBM Watsonx Orchestrate that creates tickets from email processor payloads and handles the complete ticket creation workflow including booking acknowledgements and UPI submissions.

**Note: All code is self-contained in the `greeter_agent` folder. No dependencies on external `/tools` folder.**

## Overview

The Greeter Agent receives processed email data from the Email Processor and:
1. Creates tickets from JSON payloads via CRM API
2. Handles booking acknowledgement workflows
3. Manages UPI ID collection for refunds
4. Provides follow-up messaging
5. Sends email notifications to customers

## Architecture

```
Email Processor → Webhook POST → Greeter Agent Server → IBM Watsonx Orchestrate Agent → Tools (in greeter_agent)
```

## Components

All components are in the `greeter_agent` folder:

- **`server.py`**: Flask server that receives webhooks from email_processor and interacts with the Orchestrate agent
- **`greeter_tools.py`**: Tool definitions for the agent (ticket creation, booking acknowledgement, UPI submission) - **self-contained, no external dependencies**
- **`greeter.yaml`**: Agent configuration file for IBM Watsonx Orchestrate
- **`email_sender.py`**: Email notification module that sends emails to customers
- **`crm_email_generator.py`**: CRM API integration for generating enriched email responses
- **`followup_worker.py`**: Background worker for delayed follow-up messages

## Prerequisites

- Python 3.11, 3.12, or 3.13
- IBM Watsonx Orchestrate account access
- CRM Server running (default: http://localhost:8080) or production CRM API
- Gmail API credentials (for email notifications)

## Installation

1. Install dependencies:
```bash
cd greeter_agent
pip install -r requirements.txt
```

2. Set up environment variables (create a `.env` file or export them):
```bash
# IBM Watsonx Orchestrate
export ORCHESTRATE_URL="https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/7983dce8-73d5-4ac1-b2ad-1d74de2fc994m"
export ORCHESTRATE_API_KEY="qjBx5pUvGW9pRPuZW6Eq_rF6x2Ch5iyJpFS8IumPZq2m"
export AGENT_NAME="greeter"

# CRM Server (local or production)
export CRM_SERVER_URL="https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver"  # or production URL

# Server Configuration
export WEBHOOK_PORT=5000
export WEBHOOK_HOST="0.0.0.0"

# Gmail API (for email notifications)
export GMAIL_ACCESS_TOKEN="your-token"
export GMAIL_SENDER_EMAIL="noreply-sherlox@gmail.com"
```

## Deployment to IBM Watsonx Orchestrate

### Method 1: Via UI

1. Log in to IBM Watsonx Orchestrate
2. Navigate to Agents section
3. Click "Create Agent" or "Import Agent"
4. Upload `greeter.yaml` as the agent configuration
5. Upload `greeter_tools.py` as the tools file (all tools are self-contained in this file)
6. Configure environment variables if needed
7. Deploy the agent

### Method 2: Via CLI

```bash
# Install Orchestrate CLI
pip install --upgrade ibm-watsonx-orchestrate

# Configure environment
orchestrate env add \
  --name my-orchestrate-env \
  --url https://your-orchestrate-instance.cloud.ibm.com \
  --type ibm_iam \
  --api-key YOUR_API_KEY \
  --activate

# Import agent (from greeter_agent directory)
cd greeter_agent
orchestrate agents import -f greeter.yaml

# Upload tools (all tools are in greeter_tools.py)
orchestrate agents update --name greeter --tools-file greeter_tools.py

# Deploy
orchestrate agents deploy --name greeter
```

## Running the Server

### Start the Webhook Server

```bash
cd greeter_agent
python server.py
```

The server will start on `http://0.0.0.0:5000` (or the configured port).

### Endpoints

- **`GET /health`**: Health check endpoint
- **`POST /webhook`**: Receives payloads from email_processor
  ```json
  {
    "CustomerName": "John Doe",
    "CustomerEmail": "john@example.com",
    "CustomerPhoneNumber": "+1234567890",
    "IssueDescription": "Need help with booking cancellation",
    "Priority": "HIGH"
  }
  ```
- **`POST /chat`**: Direct chat endpoint for testing
  ```json
  {
    "message": "Your message or JSON payload here"
  }
  ```

## Integration with CRM Server

The greeter agent integrates with the CRM Server API:

- **Create Ticket**: `POST http://localhost:8080/api/tickets`
- **Get Bookings**: `GET http://localhost:8080/api/tickets/bookings?email={email}`

The CRM server URL is configurable via `CRM_SERVER_URL` environment variable (defaults to `http://localhost:8080`).

## Email Notifications

The greeter agent automatically sends email notifications to customers:

1. **Ticket Created**: When a ticket is successfully created
2. **Booking Acknowledged**: When a booking refund is acknowledged
3. **UPI Request**: When UPI ID is needed (sent by follow-up worker)
4. **Refund Reinitiated**: When refund is reinitiated after UPI submission

All emails are enriched with CRM API data (ticket references, booking details, etc.) via the `crm_email_generator.py` module.

## Tools

All tools are defined in `greeter_tools.py` and are self-contained:

- **`greeting()`**: Returns a simple greeting
- **`create_ticket_from_json(payload)`**: Creates a ticket from a JSON payload
  - Automatically sends email notification to customer when ticket is created
  - Checks for pending bookings via CRM API
- **`create_ticket_from_email(email_text, ...)`**: Extracts info from email and creates a ticket
- **`acknowledge_booking(bookingId, customerEmail, ticketReference)`**: Acknowledges a booking for refund
  - Automatically sends email notification to customer
- **`submit_upi(bookingId, customerEmail, upiId)`**: Submits UPI ID for refund processing
  - Automatically sends email notification when refund is reinitiated

## Local Development

### Using Combined Local Run Script

See the main project's `LOCAL_RUN_COMBINED.md` for instructions on running all services together.

### Standalone Testing

1. Start CRM Server (if running locally):
```bash
cd C:\Users\ANIKET R SHANKAR\Desktop\lablab_ibm\CRM-Server\orchestrate
.\mvnw.cmd spring-boot:run
```

2. Start Greeter Agent Server:
```bash
cd greeter_agent
python server.py
```

3. Test the webhook:
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/webhook" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"CustomerName":"Test User","CustomerEmail":"test@example.com","IssueDescription":"Test issue","Priority":"HIGH"}'
```

## Configuration

### Environment Variables

- `ORCHESTRATE_URL`: IBM Watsonx Orchestrate instance URL (required)
- `ORCHESTRATE_API_KEY`: IBM Watsonx Orchestrate API key (required)
- `AGENT_NAME`: Agent name (default: "greeter")
- `CRM_SERVER_URL`: CRM server URL (default: "http://localhost:8080")
- `WEBHOOK_PORT`: Webhook server port (default: 5000)
- `WEBHOOK_HOST`: Webhook server host (default: "0.0.0.0")
- `GMAIL_ACCESS_TOKEN`: Gmail API access token (for email notifications)
- `GMAIL_SENDER_EMAIL`: Email address to send from (default: "noreply-sherlox@gmail.com")

## Troubleshooting

### Agent Not Responding

- Check `ORCHESTRATE_URL` and `ORCHESTRATE_API_KEY` are set correctly
- Verify agent is deployed in IBM Watsonx Orchestrate
- Check server logs for errors

### CRM API Errors

- Verify CRM server is running (if using local server)
- Check `CRM_SERVER_URL` environment variable
- Test CRM API directly: `curl http://localhost:8080/api/tickets`

### Email Not Sending

- Check `GMAIL_ACCESS_TOKEN` is set and valid
- Verify Gmail API permissions include `gmail.send`
- Check email sender logs for errors

## File Structure

```
greeter_agent/
├── __init__.py
├── server.py                 # Flask webhook server
├── greeter_tools.py          # All agent tools (self-contained)
├── greeter.yaml              # Agent configuration
├── email_sender.py           # Email notification module
├── crm_email_generator.py    # CRM API integration for emails
├── followup_worker.py        # Follow-up message worker
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── deploy_cli.py             # Deployment CLI helper
```

**All code is self-contained in this folder. No external dependencies on `/tools` folder.**
