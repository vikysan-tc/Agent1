# Integration with Greeter Agent

This document describes how to configure the email processor to send processed emails to the greeter agent in both local and production environments.

## Overview

The email processor extracts customer information from emails and sends structured payloads to the greeter agent, which creates tickets and manages the customer support workflow.

## Configuration

### Environment Variables

The email processor uses the following environment variables to determine where to send processed emails:

- `AGENT_WEBHOOK_URL`: Primary webhook URL (takes precedence if set)
- `AGENT_WEBHOOK_URL_LOCAL`: Webhook URL for local development
- `AGENT_WEBHOOK_URL_PRODUCTION`: Webhook URL for production
- `ENVIRONMENT`: Environment setting (`local` or `production`)

### Local Development Setup

1. **Set Environment Variables:**
```bash
export ENVIRONMENT="local"
export AGENT_WEBHOOK_URL_LOCAL="http://localhost:5000/webhook"
```

Or use the main webhook URL:
```bash
export AGENT_WEBHOOK_URL="http://localhost:5000/webhook"
```

2. **Start the Greeter Agent Server:**
```bash
cd greeter_agent
export ORCHESTRATE_URL="https://your-orchestrate-instance.cloud.ibm.com"
export ORCHESTRATE_API_KEY="your-api-key"
python server.py
```

3. **Start the Email Processor:**
```bash
cd email_processor
# Configure Gmail API credentials
export GMAIL_ACCESS_TOKEN="your-token"
export GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
# Set greeter webhook
export AGENT_WEBHOOK_URL="http://localhost:5000/webhook"
python gmail_watcher.py
```

### Production Setup

1. **Set Environment Variables:**
```bash
export ENVIRONMENT="production"
export AGENT_WEBHOOK_URL_PRODUCTION="https://your-greeter-agent-server.com/webhook"
```

Or use the main webhook URL:
```bash
export AGENT_WEBHOOK_URL="https://your-greeter-agent-server.com/webhook"
```

2. **Deploy Greeter Agent Server:**
   - Deploy the greeter agent server to your production environment
   - Ensure it's accessible at the configured webhook URL
   - Configure environment variables on the server

3. **Configure Email Processor:**
   - Set `ENVIRONMENT=production`
   - Set `AGENT_WEBHOOK_URL_PRODUCTION` to your production greeter server URL
   - Deploy email processor with these environment variables

## Payload Format

The email processor sends the following JSON payload to the greeter agent:

```json
{
  "CustomerName": "John Doe",
  "CustomerEmail": "john@example.com",
  "CustomerPhoneNumber": "+1234567890",
  "IssueDescription": "I need help with my booking cancellation",
  "Priority": "HIGH",
  "Subject": "Urgent: Booking Cancellation Request",
  "EmailMetadata": {
    "From": "John Doe <john@example.com>",
    "To": "reachus.sherlox@gmail.com",
    "Subject": "Urgent: Booking Cancellation Request",
    "Date": "Mon, 1 Jan 2024 12:00:00 +0000",
    "MessageID": "message-id-123",
    "ThreadID": "thread-id-456",
    "HasSubject": true,
    "SubjectLength": 35,
    "BodyLength": 150
  }
}
```

## Flow

1. **Email Received**: Customer sends email to `reachus.sherlox@gmail.com`
2. **Email Processing**: Email processor extracts customer information
3. **Validation**: Checks if email is a complaint/error with required information
4. **Send to Greeter**: If valid, sends payload to greeter agent webhook
5. **Ticket Creation**: Greeter agent creates ticket and sends email notification
6. **Workflow**: Greeter agent manages booking acknowledgement, UPI collection, etc.

## Testing

### Test Local Integration

1. Start greeter agent server:
```bash
cd greeter_agent
python server.py
```

2. Test webhook endpoint:
```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "CustomerName": "Test User",
    "CustomerEmail": "test@example.com",
    "IssueDescription": "Test issue",
    "Priority": "HIGH"
  }'
```

3. Send a test email to `reachus.sherlox@gmail.com` and verify:
   - Email processor processes it
   - Payload is sent to greeter agent
   - Ticket is created
   - Customer receives email notification

## Troubleshooting

### Email Processor Not Sending to Greeter

1. Check environment variables:
```bash
echo $ENVIRONMENT
echo $AGENT_WEBHOOK_URL
echo $AGENT_WEBHOOK_URL_LOCAL
echo $AGENT_WEBHOOK_URL_PRODUCTION
```

2. Check greeter agent server is running:
```bash
curl http://localhost:5000/health
```

3. Check email processor logs for errors

### Greeter Agent Not Receiving Payloads

1. Verify webhook URL is correct
2. Check greeter agent server logs
3. Test webhook endpoint directly with curl
4. Verify network connectivity between services

### Email Notifications Not Sending

1. Check Gmail API credentials in greeter agent:
```bash
echo $GMAIL_ACCESS_TOKEN
echo $GMAIL_SENDER_EMAIL
```

2. Verify Gmail API permissions
3. Check greeter agent logs for email sending errors

