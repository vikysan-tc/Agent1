# IBM Watsonx Orchestrate Agents

This repository contains two IBM Watsonx Orchestrate agents:

1. **Greetings Agent** - Handles greetings and ticket creation
2. **Email Processor Agent** - Monitors Gmail and processes emails to extract customer information

## Quick Start

### Greetings Agent
```bash
cd greetings
pip install -r requirements.txt
# Deploy greeter.yaml and greetings.py to IBM Watsonx Orchestrate
```

### Email Processor Agent
```bash
cd email_processor
pip install -r requirements.txt
python setup_gmail_auth.py  # First time setup for Gmail API
# Configure environment variables (see email_processor/README.md)
# Deploy email_processor.yaml and email_processor.py to IBM Watsonx Orchestrate
```

## Project Structure

```
Agent1/
├── greetings/                    # Greetings Agent
│   ├── greetings.py             # Tool definitions
│   ├── greeter.yaml             # Agent configuration
│   ├── requirements.txt        # Dependencies
│   └── README.md               # Documentation
│
├── email_processor/             # Email Processor Agent
│   ├── email_processor.py      # Tool definitions
│   ├── email_processor.yaml    # Agent configuration
│   ├── gmail_watcher.py        # Gmail monitoring (standalone)
│   ├── setup_gmail_auth.py     # Gmail API setup
│   ├── requirements.txt        # Dependencies
│   └── README.md              # Documentation
│
├── DEPLOYMENT_CHECKLIST.md     # Complete deployment guide
└── POST_DEPLOYMENT_SHARING_LIST.md  # Items to share post-deployment
```

## Features

### Greetings Agent
- Simple greeting functionality
- Ticket creation from JSON payloads
- Ticket creation from email text
- Booking acknowledgement workflow
- UPI submission for refunds

### Email Processor Agent
- **Gmail Integration**: Monitors `reachus.sherlox@gmail.com` for new emails
- **Email Processing**: Extracts customer name, email, phone, and issue description
- **Priority Detection**: Automatically determines priority (HIGH/MEDIUM/LOW)
- **Structured Output**: Creates payloads in the exact format:
  ```json
  {
      "CustomerName": "Logan Paul",
      "CustomerEmail": "logan@example.com",
      "CustomerPhoneNumber": "555-1234",
      "IssueDescription": "Need refund for cancelled booking",
      "Priority": "HIGH"
  }
  ```
- **Agent Integration**: Sends processed payloads to another agent via webhook

## Documentation

- **Greetings Agent**: See `greetings/README.md`
- **Email Processor Agent**: See `email_processor/README.md`
- **Deployment Guide**: See `DEPLOYMENT_CHECKLIST.md`
- **Sharing List**: See `POST_DEPLOYMENT_SHARING_LIST.md`

## Requirements

- Python 3.13
- IBM Watsonx Orchestrate account
- Gmail API credentials (for Email Processor)
- Google Cloud Console project with Gmail API enabled

## Deployment

See `DEPLOYMENT_CHECKLIST.md` for detailed step-by-step deployment instructions.

## Support

For issues or questions:
1. Check the README files in each agent folder
2. Review `DEPLOYMENT_CHECKLIST.md` for troubleshooting
3. Check IBM Watsonx Orchestrate documentation
4. Review Gmail API documentation for email-related issues

