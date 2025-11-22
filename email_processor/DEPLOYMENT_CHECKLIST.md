# Deployment Checklist for IBM Watsonx Orchestrate Agents

This document provides a comprehensive checklist for deploying both the **Greetings Agent** and **Email Processor Agent** to IBM Watsonx Orchestrate.

## Pre-Deployment Requirements

### For Greetings Agent

- [ ] IBM Watsonx Orchestrate account access
- [ ] Python 3.13 installed
- [ ] `ibm-watsonx-orchestrate` package installed
- [ ] Access to the ticket API endpoint (if applicable)
- [ ] Network access to external APIs

### For Email Processor Agent

- [ ] All requirements from Greetings Agent
- [ ] Google Cloud Console account
- [ ] Gmail API enabled in Google Cloud project
- [ ] OAuth 2.0 credentials created and downloaded
- [ ] Gmail account access for `reachus.sherlox@gmail.com`
- [ ] Webhook URL or API endpoint for sending processed emails to another agent

## Deployment Steps

### 1. Greetings Agent Deployment

#### Step 1.1: Prepare Files
- [ ] Navigate to `greetings/` directory
- [ ] Verify `greetings.py` contains all required tools
- [ ] Verify `greeter.yaml` configuration is correct
- [ ] Check `requirements.txt` has all dependencies

#### Step 1.2: Install Dependencies
```bash
cd greetings
pip install -r requirements.txt
```

#### Step 1.3: Deploy to Orchestrate
- [ ] Log in to IBM Watsonx Orchestrate
- [ ] Create a new agent or select existing agent
- [ ] Upload `greeter.yaml` as agent configuration
- [ ] Upload `greetings.py` as the tools file
- [ ] Configure any required environment variables
- [ ] Test the agent with sample inputs

#### Step 1.4: Verify Deployment
- [ ] Test `greeting` tool
- [ ] Test `create_ticket_from_json` with sample payload
- [ ] Test `create_ticket_from_email` with sample email
- [ ] Verify ticket creation API integration (if applicable)

### 2. Email Processor Agent Deployment

#### Step 2.1: Gmail API Setup
- [ ] Go to [Google Cloud Console](https://console.cloud.google.com/)
- [ ] Create a new project or select existing project
- [ ] Enable Gmail API:
  - Navigate to "APIs & Services" → "Library"
  - Search for "Gmail API"
  - Click "Enable"
- [ ] Create OAuth 2.0 credentials:
  - Go to "APIs & Services" → "Credentials"
  - Click "Create Credentials" → "OAuth 2.0 Client ID"
  - Application type: "Desktop app" or "Web application"
  - Download credentials JSON file
- [ ] Configure OAuth consent screen (if not already done):
  - Go to "APIs & Services" → "OAuth consent screen"
  - Fill in required information
  - Add test users if in testing mode

#### Step 2.2: Get Gmail Access Token
- [ ] Download `credentials.json` from Google Cloud Console
- [ ] Place `credentials.json` in `email_processor/` directory
- [ ] Run authentication script:
  ```bash
  cd email_processor
  python setup_gmail_auth.py
  ```
- [ ] Copy the access token and refresh token from output
- [ ] Save tokens securely (you'll need them for environment variables)

#### Step 2.3: Configure Environment Variables
Set the following environment variables in your deployment environment:

**Required:**
- [ ] `GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"`
- [ ] `GMAIL_ACCESS_TOKEN="<your_access_token>"` OR
- [ ] `GMAIL_REFRESH_TOKEN="<your_refresh_token>"`
- [ ] `GMAIL_CLIENT_ID="<your_client_id>"`
- [ ] `GMAIL_CLIENT_SECRET="<your_client_secret>"`

**Optional:**
- [ ] `AGENT_WEBHOOK_URL="<webhook_url_for_another_agent>"`
- [ ] `GMAIL_POLL_INTERVAL="60"` (default: 60 seconds)

#### Step 2.4: Prepare Files
- [ ] Navigate to `email_processor/` directory
- [ ] Verify `email_processor.py` contains all required tools
- [ ] Verify `email_processor.yaml` configuration is correct
- [ ] Check `requirements.txt` has all dependencies
- [ ] Review `gmail_watcher.py` (for standalone mode, if needed)

#### Step 2.5: Install Dependencies
```bash
cd email_processor
pip install -r requirements.txt
```

#### Step 2.6: Deploy to Orchestrate
- [ ] Log in to IBM Watsonx Orchestrate
- [ ] Create a new agent or select existing agent
- [ ] Upload `email_processor.yaml` as agent configuration
- [ ] Upload `email_processor.py` as the tools file
- [ ] Configure environment variables in Orchestrate:
  - Gmail API credentials
  - Webhook URL for sending to another agent
  - Polling interval (if using polling mode)
- [ ] Test the agent with sample email data

#### Step 2.7: Set Up Gmail Watcher (Optional)
If you want to run the Gmail watcher as a separate service:

- [ ] Set up a cron job or scheduled task to run `gmail_watcher.py`
- [ ] Or run it as a background service:
  ```bash
  python gmail_watcher.py
  ```
- [ ] Verify it's processing emails correctly

#### Step 2.8: Verify Deployment
- [ ] Send a test email to `reachus.sherlox@gmail.com`
- [ ] Verify email is processed by the agent
- [ ] Check that payload is created in correct format:
  ```json
  {
      "CustomerName": "...",
      "CustomerEmail": "...",
      "CustomerPhoneNumber": "...",
      "IssueDescription": "...",
      "Priority": "HIGH|MEDIUM|LOW"
  }
  ```
- [ ] Verify payload is sent to the target agent/webhook
- [ ] Test with various email formats (complaints, inquiries, etc.)

### 3. Integration Testing

#### Step 3.1: End-to-End Test
- [ ] Send email to `reachus.sherlox@gmail.com` with customer complaint
- [ ] Verify Email Processor Agent processes the email
- [ ] Verify payload is sent to Greetings Agent (or target agent)
- [ ] Verify Greetings Agent receives and processes the payload
- [ ] Verify ticket is created (if applicable)

#### Step 3.2: Error Handling
- [ ] Test with malformed emails
- [ ] Test with missing customer information
- [ ] Test with invalid Gmail credentials
- [ ] Test with webhook failures
- [ ] Verify error messages are logged appropriately

## Post-Deployment Checklist

### Monitoring and Maintenance

- [ ] Set up logging/monitoring for both agents
- [ ] Configure alerts for:
  - Gmail API authentication failures
  - Email processing failures
  - Webhook delivery failures
  - Agent downtime
- [ ] Set up regular token refresh (if using refresh tokens)
- [ ] Monitor processed emails count
- [ ] Review error logs regularly

### Security

- [ ] Ensure Gmail credentials are stored securely (use secrets management)
- [ ] Rotate access tokens regularly
- [ ] Review OAuth2 scopes (use minimum required)
- [ ] Enable 2FA on Gmail account
- [ ] Restrict webhook URL access (if applicable)
- [ ] Use HTTPS for all API communications

### Documentation

- [ ] Document agent endpoints and webhooks
- [ ] Document payload formats
- [ ] Document error codes and handling
- [ ] Create runbook for common issues
- [ ] Document escalation procedures

## Troubleshooting Guide

### Gmail API Issues
**Problem:** Authentication fails
- Check access token is valid and not expired
- Verify OAuth2 credentials are correct
- Ensure Gmail API is enabled in Google Cloud Console
- Check OAuth consent screen is configured

**Problem:** Emails not being received
- Verify email address: `reachus.sherlox@gmail.com`
- Check Gmail account has proper permissions
- Verify Gmail API scopes include `gmail.readonly`
- Check if emails are being filtered/spam

### Agent Deployment Issues
**Problem:** Tools not loading
- Verify Python file syntax is correct
- Check all imports are available
- Verify tool decorators are correct
- Check YAML configuration matches tool names

**Problem:** Environment variables not working
- Verify variables are set in Orchestrate environment
- Check variable names match exactly (case-sensitive)
- Ensure variables are available to the agent runtime

### Integration Issues
**Problem:** Payload not reaching target agent
- Verify webhook URL is correct and accessible
- Check network connectivity
- Verify payload format matches expected schema
- Review webhook response codes

## Support Contacts

- IBM Watsonx Orchestrate Support: [Add support contact]
- Gmail API Support: [Google Cloud Support]
- Internal Team: [Add team contact]

## Additional Notes

- The Email Processor Agent processes emails sent to `reachus.sherlox@gmail.com` automatically
- Payloads are sent in the exact format specified:
  ```json
  {
      "CustomerName": "Logan Paul",
      "CustomerEmail": "logan@example.com",
      "CustomerPhoneNumber": "555-1234",
      "IssueDescription": "Need refund for cancelled booking",
      "Priority": "HIGH"
  }
  ```
- Priority is automatically determined based on email content keywords
- Both agents can be deployed independently or integrated together
- The Gmail watcher can run as a standalone service or be integrated into the agent

## Files to Share Post-Deployment

1. **Greetings Agent:**
   - `greetings/greetings.py`
   - `greetings/greeter.yaml`
   - `greetings/requirements.txt`

2. **Email Processor Agent:**
   - `email_processor/email_processor.py`
   - `email_processor/email_processor.yaml`
   - `email_processor/requirements.txt`
   - `email_processor/gmail_watcher.py` (optional, for standalone mode)
   - `email_processor/setup_gmail_auth.py` (for initial setup)

3. **Documentation:**
   - `DEPLOYMENT_CHECKLIST.md` (this file)
   - `email_processor/README.md`

4. **Environment Variables Template:**
   - Create a `.env.example` file with all required variables (without actual values)

