# CLI-Only Deployment Guide for Email Processor Agent

This guide provides step-by-step instructions for deploying the `email_processor` agent to IBM Watsonx Orchestrate using **only the command-line interface (CLI)**.

## Prerequisites

Before deploying, ensure you have:

- [ ] IBM Watsonx Orchestrate account access
- [ ] Python 3.11, 3.12, or 3.13 installed (Python 3.14+ is NOT supported)
- [ ] IBM Cloud API key (for authentication)
- [ ] Watsonx Orchestrate service instance URL
- [ ] Gmail API credentials configured (see [ENV_VARIABLES.md](ENV_VARIABLES.md))
- [ ] All required files in the `email_processor/` directory

## Step 1: Install IBM Watsonx Orchestrate CLI

The CLI is included in the `ibm-watsonx-orchestrate` package. Install it using pip:

```bash
# Verify Python version (must be 3.11, 3.12, or 3.13)
python --version

# Install or upgrade the package
pip install --upgrade ibm-watsonx-orchestrate

# Verify CLI is available
orchestrate --version
```

If the `orchestrate` command is not found, ensure your Python scripts directory is in your PATH, or use:
```bash
python -m ibm_watsonx_orchestrate.cli --version
```

## Step 2: Configure CLI Environment

Set up the CLI to connect to your IBM Watsonx Orchestrate instance:

```bash
# Add and activate your environment
orchestrate env add --name <your-env-name> --url <your-service-instance-url> --type ibm_iam --activate
```

**Parameters:**
- `<your-env-name>`: A descriptive name for your environment (e.g., `watsonx-prod`, `my-orchestrate-env`)
- `<your-service-instance-url>`: The URL of your Watsonx Orchestrate service instance
  - **Format**: `https://api.<region>.watson-orchestrate.cloud.ibm.com` (base URL only, without `/instances/...`)
  - If you have a full instance URL like `https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/7983dce8-...`, use only: `https://api.ca-tor.watson-orchestrate.cloud.ibm.com`
  - You can find this in your IBM Cloud dashboard

**Example:**
```bash
# If your full URL is: https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/7983dce8-73d5-4ac1-b2ad-1d74de2fc994
# Use only the base URL:
orchestrate env add --name watsonx-prod --url https://api.ca-tor.watson-orchestrate.cloud.ibm.com --type ibm_iam --activate
```

You'll be prompted to enter your **IBM Cloud API key** during this process. If you don't have one:
1. Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
2. Click "Create an IBM Cloud API key"
3. Copy the API key and paste it when prompted

**Verify environment is active:**
```bash
orchestrate env list
```

The active environment should be marked with an asterisk (*).

## Step 3: Prepare Deployment Files

Navigate to the email_processor directory and verify all files are present:

```bash
cd email_processor

# Verify required files exist
ls -la email_processor.yaml
ls -la email_processor.py
ls -la requirements.txt
```

**Required files:**
- ✅ `email_processor.yaml` - Agent configuration
- ✅ `email_processor.py` - Tool definitions (contains `process_email`, `send_to_agent`, `process_and_send_email`)
- ✅ `requirements.txt` - Python dependencies

## Step 4: Import/Create the Agent

You have two options:

### Option A: Import Agent from YAML (Recommended)

Import the agent configuration directly from the YAML file:

```bash
orchestrate agents import -f email_processor.yaml
```

This will:
- Create the agent with the name specified in the YAML (`email_processor`)
- Configure the LLM model (`watsonx/meta-llama/llama-3-2-90b-vision-instruct`)
- Set up the agent instructions
- Register the tools listed in the YAML

### Option B: Create Agent Manually

If you prefer to create the agent step by step:

```bash
# Create the agent
orchestrate agents create \
  --name email_processor \
  --kind native \
  --description "An agent that processes emails from Gmail and extracts customer information to send to another agent for analysis" \
  --llm watsonx/meta-llama/llama-3-2-90b-vision-instruct

# Then upload the tools file
orchestrate agents update --name email_processor --tools-file email_processor.py
```

**Verify agent was created:**
```bash
orchestrate agents list
```

## Step 5: Configure Environment Variables

Set the required environment variables for the agent. You'll need to provide these credentials:

### Required Environment Variables

```bash
# Gmail Configuration
GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"

# Gmail API Authentication (choose one method)
# Option 1: Direct Access Token (simpler, but expires)
GMAIL_ACCESS_TOKEN="<your_access_token>"

# Option 2: OAuth2 Refresh Token (recommended for production)
GMAIL_REFRESH_TOKEN="<your_refresh_token>"
GMAIL_CLIENT_ID="<your_client_id>"
GMAIL_CLIENT_SECRET="<your_client_secret>"

# Optional: Agent Integration
AGENT_WEBHOOK_URL="<webhook_url_for_another_agent>"
GMAIL_REPLY_EMAIL="reachus.sherlox@gmail.com"
GMAIL_POLL_INTERVAL="60"
```

### Setting Environment Variables via CLI

**Note:** The exact command may vary depending on your CLI version. Check available options:

```bash
orchestrate agents env --help
```

**Method 1: Set environment variables during agent update:**
```bash
orchestrate agents update --name email_processor \
  --env GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com" \
  --env GMAIL_ACCESS_TOKEN="<your_access_token>" \
  --env GMAIL_CLIENT_ID="<your_client_id>" \
  --env GMAIL_CLIENT_SECRET="<your_client_secret>" \
  --env AGENT_WEBHOOK_URL="<your_webhook_url>"
```

**Method 2: Use a JSON file for environment variables:**

Create a file `env_vars.json`:
```json
{
  "GMAIL_WATCH_EMAIL": "reachus.sherlox@gmail.com",
  "GMAIL_ACCESS_TOKEN": "<your_access_token>",
  "GMAIL_CLIENT_ID": "<your_client_id>",
  "GMAIL_CLIENT_SECRET": "<your_client_secret>",
  "AGENT_WEBHOOK_URL": "<your_webhook_url>",
  "GMAIL_REPLY_EMAIL": "reachus.sherlox@gmail.com",
  "GMAIL_POLL_INTERVAL": "60"
}
```

Then apply it:
```bash
orchestrate agents update --name email_processor --env-file env_vars.json
```

**Method 3: If CLI doesn't support env vars directly, use the API:**

You may need to use the REST API or SDK. See "Alternative: Using Python SDK" section below.

## Step 6: Upload Tools File

If you created the agent manually (Option B), upload the tools file:

```bash
orchestrate agents update --name email_processor --tools-file email_processor.py
```

Or if using a different command format:
```bash
orchestrate agents tools upload --name email_processor --file email_processor.py
```

## Step 7: Verify Agent Configuration

Check that the agent is configured correctly:

```bash
# List all agents
orchestrate agents list

# Get agent details
orchestrate agents get --name email_processor

# List agent tools
orchestrate agents tools list --name email_processor
```

You should see:
- Agent name: `email_processor`
- Status: `draft` or `active`
- Tools: `process_email`, `send_to_agent`, `process_and_send_email`

## Step 8: Deploy the Agent

Deploy the agent to make it live:

```bash
orchestrate agents deploy --name email_processor
```

This command transitions the agent from a draft state to a live/active state.

**Verify deployment:**
```bash
orchestrate agents get --name email_processor
```

The status should show `active` or `deployed`.

## Step 9: Test the Agent

Test the deployed agent:

```bash
# Test with a sample message
orchestrate agents chat --name email_processor --message "Test the process_email tool with sample email data"

# Or test a specific tool
orchestrate agents tools test --name email_processor --tool process_email --input '{"email_text": "From: John Doe <john@example.com>\nSubject: Refund Request\nBody: I need a refund."}'
```

## Alternative: Using Python SDK (If CLI is Limited)

If the CLI doesn't support all features (like environment variables), you can use the Python SDK:

```python
from ibm_watsonx_orchestrate import OrchestrateClient
import os

# Initialize client
client = OrchestrateClient(
    api_key=os.environ.get('IBM_CLOUD_API_KEY'),
    service_url=os.environ.get('WATSONX_SERVICE_URL')
)

# Create or update agent
agent_config = {
    'name': 'email_processor',
    'kind': 'native',
    'description': 'Email processor agent',
    'llm': 'watsonx/meta-llama/llama-3-2-90b-vision-instruct',
    'tools': ['process_email', 'send_to_agent', 'process_and_send_email']
}

# Read YAML file
with open('email_processor.yaml', 'r') as f:
    yaml_content = f.read()

# Create agent
agent = client.agents.create(config=yaml_content)

# Set environment variables
env_vars = {
    'GMAIL_WATCH_EMAIL': 'reachus.sherlox@gmail.com',
    'GMAIL_ACCESS_TOKEN': '<your_token>',
    'GMAIL_CLIENT_ID': '<your_client_id>',
    'GMAIL_CLIENT_SECRET': '<your_client_secret>',
    'AGENT_WEBHOOK_URL': '<your_webhook_url>'
}

client.agents.update_env_vars(agent_id=agent['id'], env_vars=env_vars)

# Upload tools file
with open('email_processor.py', 'r') as f:
    tools_content = f.read()

client.agents.update_tools(agent_id=agent['id'], tools_file=tools_content)

# Deploy
client.agents.deploy(agent_id=agent['id'])
```

## Troubleshooting

### CLI Command Not Found

```bash
# Try using Python module directly
python -m ibm_watsonx_orchestrate.cli --version

# Or add Python scripts to PATH
# Windows:
set PATH=%PATH%;%APPDATA%\Python\Python3XX\Scripts
# Linux/Mac:
export PATH=$PATH:~/.local/bin
```

### Authentication Errors

```bash
# Re-authenticate
orchestrate env remove --name <your-env-name>
orchestrate env add --name <your-env-name> --url <your-url> --type ibm_iam --activate
```

### URL Format Issues

**Problem**: If you're getting errors with a URL like:
```
https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/7983dce8-73d5-4ac1-b2ad-1d74de2fc994
```

**Solution**: Use only the base URL without the `/instances/...` part:
```bash
# Wrong (includes instance path):
orchestrate env add --name prod --url https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/7983dce8-73d5-4ac1-b2ad-1d74de2fc994 --type ibm_iam --activate

# Correct (base URL only):
orchestrate env add --name prod --url https://api.ca-tor.watson-orchestrate.cloud.ibm.com --type ibm_iam --activate
```

**Note**: The instance ID (`7983dce8-73d5-4ac1-b2ad-1d74de2fc994`) is automatically detected from your API key, so you don't need to include it in the URL.

### Agent Import Fails

- Verify YAML syntax is correct: `python -c "import yaml; yaml.safe_load(open('email_processor.yaml'))"`
- Check that all required fields are present in the YAML
- Ensure the LLM model name is correct

### Environment Variables Not Working

- Verify variable names match exactly (case-sensitive)
- Check that variables are set in the agent's environment, not just your local shell
- Use `orchestrate agents get --name email_processor` to verify configuration

### Tools Not Loading

- Verify `email_processor.py` has correct `@tool` decorators
- Check that tool names in YAML match function names in Python file
- Ensure all imports are available (dependencies from `requirements.txt`)

## Quick Reference: Complete Deployment Command Sequence

```bash
# 1. Install CLI
pip install --upgrade ibm-watsonx-orchestrate

# 2. Configure environment
orchestrate env add --name watsonx-prod --url <your-url> --type ibm_iam --activate

# 3. Navigate to directory
cd email_processor

# 4. Import agent
orchestrate agents import -f email_processor.yaml

# 5. Set environment variables (adjust command based on your CLI version)
orchestrate agents update --name email_processor \
  --env GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com" \
  --env GMAIL_ACCESS_TOKEN="<token>" \
  --env GMAIL_CLIENT_ID="<client_id>" \
  --env GMAIL_CLIENT_SECRET="<secret>" \
  --env AGENT_WEBHOOK_URL="<webhook>"

# 6. Upload tools (if not included in import)
orchestrate agents update --name email_processor --tools-file email_processor.py

# 7. Deploy
orchestrate agents deploy --name email_processor

# 8. Verify
orchestrate agents get --name email_processor
```

## Getting Help

- **CLI Help**: `orchestrate --help` or `orchestrate <command> --help`
- **IBM Documentation**: [Watsonx Orchestrate Developer Docs](https://developer.watson-orchestrate.ibm.com/)
- **Community**: [IBM Community Forums](https://community.ibm.com/)

## Next Steps

After successful deployment:

1. **Test the Agent**: Use the chat interface or CLI to test all three tools
2. **Monitor Logs**: Check agent logs for any errors
3. **Set Up Gmail Watcher**: Configure continuous email monitoring (see `gmail_watcher.py`)
4. **Integrate with Other Agents**: Configure `AGENT_WEBHOOK_URL` to send to another agent

## Credentials Needed

To complete the deployment, you'll need to provide:

1. **IBM Cloud API Key**: For authenticating with Watsonx Orchestrate
2. **Watsonx Orchestrate Service URL**: Your service instance URL
3. **Gmail API Credentials**:
   - `GMAIL_ACCESS_TOKEN` OR (`GMAIL_REFRESH_TOKEN` + `GMAIL_CLIENT_ID` + `GMAIL_CLIENT_SECRET`)
4. **Optional**: `AGENT_WEBHOOK_URL` for integration with other agents

Share these credentials when ready, and I can help you complete the deployment!

