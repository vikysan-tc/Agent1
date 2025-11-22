# Post-Code Creation Sharing List

This document lists all the items you need to share after the code has been created for deploying the IBM Watsonx Orchestrate agents.

## Files to Share

### 1. Greetings Agent Files

Share the entire `greetings/` folder containing:

- **`greetings.py`** - Main Python file with all tool definitions
  - Contains: greeting, create_ticket, create_ticket_from_email, create_ticket_from_json, acknowledge_booking, submit_upi tools
  
- **`greeter.yaml`** - Agent configuration file
  - Defines agent name, description, instructions, LLM model, and tools
  
- **`requirements.txt`** - Python dependencies
  - ibm-watsonx-orchestrate
  - requests

- **`README.md`** - Documentation for the greetings agent

### 2. Email Processor Agent Files

Share the entire `email_processor/` folder containing:

- **`email_processor.py`** - Main Python file with email processing tools
  - Contains: process_email, send_to_agent, process_and_send_email tools
  - Extracts customer information from emails
  - Creates structured payloads in the required format
  
- **`email_processor.yaml`** - Agent configuration file
  - Defines agent name, description, instructions, LLM model, and tools
  - Configured to process emails sent to reachus.sherlox@gmail.com
  
- **`gmail_watcher.py`** - Gmail API integration script (optional, for standalone mode)
  - Monitors Gmail inbox for new emails
  - Processes emails and sends to agent
  - Can run as a background service
  
- **`setup_gmail_auth.py`** - Gmail API authentication setup script
  - Helps set up OAuth2 authentication
  - Generates access tokens for Gmail API
  
- **`requirements.txt`** - Python dependencies
  - ibm-watsonx-orchestrate
  - requests
  - google-auth
  - google-auth-oauthlib
  - google-auth-httplib2
  - google-api-python-client

- **`README.md`** - Comprehensive documentation for email processor
  - Setup instructions
  - Gmail API configuration
  - Environment variables
  - Troubleshooting guide

- **`.env.example`** - Environment variables template (if created)
  - Shows all required environment variables
  - Can be used as a template for actual configuration

### 3. Documentation Files

- **`DEPLOYMENT_CHECKLIST.md`** - Complete deployment checklist
  - Step-by-step deployment instructions
  - Pre-deployment requirements
  - Post-deployment verification
  - Troubleshooting guide

- **`POST_DEPLOYMENT_SHARING_LIST.md`** - This file
  - Lists all items to share
  - Provides context for each file

## Information to Share

### Gmail API Setup Requirements

Share the following information about Gmail API setup:

1. **Google Cloud Console Setup:**
   - Project ID
   - Gmail API enabled status
   - OAuth 2.0 credentials location/instructions

2. **OAuth2 Credentials:**
   - Client ID (can be shared, not sensitive)
   - Client Secret (SENSITIVE - share securely)
   - Redirect URIs configured

3. **Gmail Account:**
   - Email address: `reachus.sherlox@gmail.com`
   - Access permissions required
   - 2FA status (if applicable)

### Environment Variables to Configure

Share the list of required environment variables:

**For Email Processor:**
- `GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com`
- `GMAIL_ACCESS_TOKEN=<token>` (or use refresh token flow)
- `GMAIL_REFRESH_TOKEN=<token>` (if using refresh token)
- `GMAIL_CLIENT_ID=<id>` (if using refresh token)
- `GMAIL_CLIENT_SECRET=<secret>` (if using refresh token)
- `AGENT_WEBHOOK_URL=<url>` (URL to send processed emails)
- `GMAIL_POLL_INTERVAL=60` (optional)

**For Greetings Agent:**
- Any API endpoints or credentials if required
- Ticket API URL (if different from default)

### Integration Details

Share information about:

1. **Target Agent/Endpoint:**
   - Webhook URL where processed emails should be sent
   - API endpoint format expected
   - Authentication requirements (if any)

2. **Payload Format:**
   - Confirm the exact payload structure:
     ```json
     {
         "CustomerName": "Logan Paul",
         "CustomerEmail": "logan@example.com",
         "CustomerPhoneNumber": "555-1234",
         "IssueDescription": "Need refund for cancelled booking",
         "Priority": "HIGH"
     }
     ```

3. **Email Processing:**
   - Confirmation that emails sent to `reachus.sherlox@gmail.com` will be processed
   - Expected processing frequency
   - Error handling requirements

## Deployment Instructions Summary

Share a brief summary of deployment steps:

1. **Greetings Agent:**
   - Install dependencies from `requirements.txt`
   - Deploy `greeter.yaml` and `greetings.py` to Orchestrate
   - Test with sample inputs

2. **Email Processor Agent:**
   - Set up Gmail API credentials
   - Run `setup_gmail_auth.py` to get access token
   - Configure environment variables
   - Install dependencies from `requirements.txt`
   - Deploy `email_processor.yaml` and `email_processor.py` to Orchestrate
   - Optionally run `gmail_watcher.py` as a background service
   - Test by sending email to `reachus.sherlox@gmail.com`

## Security Considerations

When sharing, ensure:

- [ ] Client secrets are shared securely (not in plain text)
- [ ] Access tokens are shared securely (they expire, so refresh tokens are better)
- [ ] Webhook URLs are shared securely if they contain sensitive information
- [ ] Use secure channels for sharing credentials
- [ ] Consider using secrets management tools instead of sharing directly

## Testing Checklist to Share

Share the testing checklist:

- [ ] Send test email to `reachus.sherlox@gmail.com`
- [ ] Verify email is processed by Email Processor Agent
- [ ] Verify payload format matches specification
- [ ] Verify payload is sent to target agent/webhook
- [ ] Test with various email formats (complaints, inquiries, etc.)
- [ ] Test error handling (malformed emails, missing info, etc.)
- [ ] Verify priority detection works correctly

## Support Information

Share contact information for:

- IBM Watsonx Orchestrate support
- Gmail API/Google Cloud support
- Internal team contacts
- Escalation procedures

## Additional Notes

- Both agents can be deployed independently
- The Email Processor automatically processes emails sent to `reachus.sherlox@gmail.com`
- The Gmail watcher can run standalone or be integrated into the agent
- All code is ready for deployment to IBM Watsonx Orchestrate
- The payload format matches the exact specification provided

## Quick Start Commands

Share these quick start commands:

```bash
# Greetings Agent
cd greetings
pip install -r requirements.txt
# Then deploy via Orchestrate UI/CLI

# Email Processor Agent
cd email_processor
pip install -r requirements.txt
python setup_gmail_auth.py  # First time setup
# Configure environment variables
# Then deploy via Orchestrate UI/CLI
# Optionally: python gmail_watcher.py  # For standalone mode
```

## File Structure Summary

```
Agent1/
├── greetings/
│   ├── greetings.py
│   ├── greeter.yaml
│   ├── requirements.txt
│   └── README.md
├── email_processor/
│   ├── email_processor.py
│   ├── email_processor.yaml
│   ├── gmail_watcher.py
│   ├── setup_gmail_auth.py
│   ├── requirements.txt
│   ├── README.md
│   └── .env.example
├── DEPLOYMENT_CHECKLIST.md
└── POST_DEPLOYMENT_SHARING_LIST.md
```

---

**Note:** Ensure all sensitive information (tokens, secrets, credentials) is shared through secure channels and not included in version control or shared documentation.

