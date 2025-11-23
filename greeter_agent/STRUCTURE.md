# Greeter Agent Structure

## Self-Contained Architecture

**All code for the greeter agent is self-contained in the `greeter_agent` folder. There are NO dependencies on the `/tools` folder or any external tool files.**

## File Organization

```
greeter_agent/
├── __init__.py                    # Python package marker
├── server.py                      # Flask webhook server (main entry point)
├── greeter_tools.py               # ALL agent tools (self-contained)
├── greeter.yaml                   # Agent configuration for IBM Watsonx Orchestrate
├── email_sender.py                # Email notification module
├── crm_email_generator.py         # CRM API integration for enriched emails
├── followup_worker.py             # Background worker for delayed messages
├── deploy_cli.py                  # CLI helper for deployment
├── requirements.txt               # Python dependencies
├── README.md                      # Main documentation
└── STRUCTURE.md                   # This file
```

## Key Files

### `greeter_tools.py`
- **Contains ALL agent tools** - no external dependencies
- Tools defined:
  - `greeting()` - Simple greeting function
  - `create_ticket()` - Creates ticket via CRM API
  - `create_ticket_from_email()` - Extracts info from email and creates ticket
  - `create_ticket_from_json()` - Creates ticket from JSON payload
  - `acknowledge_booking()` - Acknowledges booking for refund
  - `submit_upi()` - Submits UPI ID for refund processing
- Uses CRM API (configurable via `CRM_SERVER_URL` environment variable)
- Integrates with `email_sender.py` for notifications

### `server.py`
- Flask webhook server
- Receives payloads from email processor
- Communicates with IBM Watsonx Orchestrate agent
- Uses tools from `greeter_tools.py` (same folder)

### `email_sender.py`
- Sends email notifications to customers
- Uses Gmail API
- Integrates with `crm_email_generator.py` for enriched content
- Called by tools in `greeter_tools.py`

### `crm_email_generator.py`
- Fetches data from CRM API
- Generates enriched email content
- Used by `email_sender.py` to create personalized emails

## Integration Points

### With Email Processor
- Receives webhook POST requests at `/webhook` endpoint
- Processes JSON payloads from email processor
- All processing uses tools in `greeter_tools.py`

### With CRM Server
- Creates tickets via `POST /api/tickets`
- Fetches bookings via `GET /api/tickets/bookings?email={email}`
- CRM URL configurable via `CRM_SERVER_URL` environment variable
- Default: `http://localhost:8080` (local development)

### With IBM Watsonx Orchestrate
- Agent deployed to Orchestrate platform
- Uses `greeter.yaml` for configuration
- Uses `greeter_tools.py` for all tools
- Server communicates via Orchestrate REST API

## Environment Variables

All configuration is done via environment variables:

```bash
# Required
ORCHESTRATE_URL=https://your-instance.cloud.ibm.com
ORCHESTRATE_API_KEY=your-api-key

# Optional (with defaults)
CRM_SERVER_URL=http://localhost:8080
AGENT_NAME=greeter
WEBHOOK_PORT=5000
WEBHOOK_HOST=0.0.0.0
GMAIL_ACCESS_TOKEN=your-token
GMAIL_SENDER_EMAIL=noreply-sherlox@gmail.com
```

## No External Dependencies

- ❌ **NO** dependency on `/tools` folder
- ❌ **NO** dependency on root `greetings.py`
- ✅ **ALL** code is in `greeter_agent` folder
- ✅ **ALL** tools are in `greeter_tools.py`
- ✅ **SELF-CONTAINED** - can be deployed independently

## Deployment

When deploying to IBM Watsonx Orchestrate:

1. Upload `greeter.yaml` - agent configuration
2. Upload `greeter_tools.py` - all tools (self-contained)
3. Set environment variables
4. Deploy

**No need to upload anything from `/tools` folder or root directory.**

## Local Development

When running locally:

1. All code is in `greeter_agent` folder
2. Set environment variables
3. Run `python server.py`
4. Tools are automatically loaded from `greeter_tools.py`

**No need to reference `/tools` folder or any external tool files.**

