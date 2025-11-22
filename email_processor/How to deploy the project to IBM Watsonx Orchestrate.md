# How to Deploy the Project to IBM Watsonx Orchestrate

This guide provides step-by-step instructions for deploying the Email Processor Agent to IBM Watsonx Orchestrate.

## Prerequisites

- IBM Watsonx Orchestrate account access
- Python 3.11, 3.12, or 3.13 installed
- `ibm-watsonx-orchestrate` package installed
- Gmail API credentials configured (see local setup guide)
- All environment variables prepared

## Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] Gmail API enabled in Google Cloud Console
- [ ] OAuth 2.0 credentials created and downloaded
- [ ] Gmail access token or refresh token obtained
- [ ] All required files in the `email_processor` directory:
  - [ ] `email_processor.py` (agent tools)
  - [ ] `email_processor.yaml` (agent configuration)
  - [ ] `requirements.txt` (dependencies)
- [ ] Environment variables documented and ready

## Deployment Methods

There are two ways to deploy the agent:
1. **Via IBM Watsonx Orchestrate UI** (Recommended for first-time deployment)
2. **Via CLI** (Automated deployment)

## Method 1: Deploy via UI

### Step 1: Prepare Files

Ensure you have the following files ready:
- `email_processor.yaml` - Agent configuration
- `email_processor.py` - Agent tools implementation
- `requirements.txt` - Python dependencies

### Step 2: Log in to IBM Watsonx Orchestrate

1. Navigate to your IBM Watsonx Orchestrate instance
2. Log in with your IBM Cloud credentials
3. Navigate to the Agents section

### Step 3: Create New Agent

1. Click **Create Agent** or **Import Agent**
2. Select **Import from YAML** or **Upload Configuration**
3. Upload `email_processor.yaml` file

### Step 4: Upload Tools File

1. In the agent configuration, navigate to **Tools** section
2. Upload `email_processor.py` as the tools file
3. Verify all tools are recognized:
   - `process_email`
   - `send_to_agent`
   - `process_and_send_email`

### Step 5: Configure Environment Variables

In the agent settings, add the following environment variables:

#### Required Variables

```
GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
GMAIL_ACCESS_TOKEN=ya29.a0AfH6SMBx...
```

**OR** (for production with refresh tokens):

```
GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
GMAIL_REFRESH_TOKEN=1//0g...
GMAIL_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-abc...
```

#### Optional Variables

```
AGENT_WEBHOOK_URL=https://your-webhook-url.com/api/process
GMAIL_REPLY_EMAIL=reachus.sherlox@gmail.com
GMAIL_POLL_INTERVAL=60
```

**Important:** Store sensitive values (tokens, secrets) in IBM Cloud Secrets Manager or use secure environment variable storage provided by Orchestrate.

### Step 6: Configure Dependencies

1. In the agent configuration, specify Python version: **3.11**, **3.12**, or **3.13**
2. Upload or reference `requirements.txt` to install dependencies
3. Ensure all packages from `requirements.txt` are installed

### Step 7: Deploy Agent

1. Review all configuration settings
2. Click **Deploy** or **Save and Deploy**
3. Wait for deployment to complete
4. Check deployment status and logs

### Step 8: Test Deployment

1. Use the agent chat interface to test tools:
   ```
   Test: process_email with sample email text
   ```
2. Verify tools execute correctly
3. Check logs for any errors
4. Test with actual Gmail integration if possible

## Method 2: Deploy via CLI

### Step 1: Install Orchestrate CLI

```bash
pip install --upgrade ibm-watsonx-orchestrate
```

Verify installation:
```bash
orchestrate --version
```

### Step 2: Set Up Environment

Configure your Orchestrate environment:

```bash
orchestrate env add \
  --name my-orchestrate-env \
  --url https://your-orchestrate-instance.cloud.ibm.com \
  --type ibm_iam \
  --api-key YOUR_API_KEY \
  --activate
```

### Step 3: Use Deployment Script

The project includes a deployment script `deploy_cli.py`:

```bash
cd email_processor
python deploy_cli.py \
  --env-name my-orchestrate-env \
  --service-url https://your-orchestrate-instance.cloud.ibm.com \
  --api-key YOUR_API_KEY \
  --agent-name email_processor \
  --env-vars-file env_vars.json
```

### Step 4: Manual CLI Deployment

If you prefer manual CLI commands:

#### Import Agent Configuration

```bash
orchestrate agents import -f email_processor.yaml
```

#### Set Environment Variables

```bash
orchestrate agents update \
  --name email_processor \
  --env GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com \
  --env GMAIL_ACCESS_TOKEN=ya29.a0AfH6SMBx...
```

Or use a JSON file:
```bash
orchestrate agents update \
  --name email_processor \
  --env-file env_vars.json
```

#### Upload Tools File

```bash
orchestrate agents update \
  --name email_processor \
  --tools-file email_processor.py
```

#### Deploy Agent

```bash
orchestrate agents deploy --name email_processor
```

## Post-Deployment Verification

### 1. Verify Agent Status

```bash
orchestrate agents get --name email_processor
```

Or check in the UI for agent status.

### 2. Test Agent Tools

Test each tool individually:

**Test process_email:**
```bash
orchestrate agents chat \
  --name email_processor \
  --message "Use process_email tool with sample email: From: John Doe <john@example.com>, Subject: Test, Body: This is a test email"
```

**Test send_to_agent:**
```bash
orchestrate agents chat \
  --name email_processor \
  --message "Use send_to_agent tool with a test payload"
```

### 3. Monitor Logs

Check agent logs for:
- Successful tool executions
- Gmail API connection status
- Email processing activities
- Any errors or warnings

### 4. Test End-to-End Flow

1. Send a test email to `reachus.sherlox@gmail.com`
2. Wait for processing (if using polling mode)
3. Verify payload is created correctly
4. Check webhook receives the payload (if configured)

## Configuration Details

### Agent Configuration (email_processor.yaml)

The YAML file defines:
- Agent name and description
- Tool definitions and schemas
- Input/output specifications
- Runtime configuration

### Tools Implementation (email_processor.py)

Contains three main tools:

1. **`process_email`**: Extracts customer information from email text
   - Input: Email text (string)
   - Output: Structured payload with customer details

2. **`send_to_agent`**: Sends processed payload to webhook/agent
   - Input: Payload dictionary
   - Output: Success/error status

3. **`process_and_send_email`**: Combines processing and sending
   - Input: Email text (string)
   - Output: Processing and sending status

### Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GMAIL_WATCH_EMAIL` | Yes | Gmail address to monitor | `reachus.sherlox@gmail.com` |
| `GMAIL_ACCESS_TOKEN` | Yes* | Gmail API access token | `ya29.a0AfH6SMBx...` |
| `GMAIL_REFRESH_TOKEN` | Yes* | OAuth2 refresh token | `1//0g...` |
| `GMAIL_CLIENT_ID` | Yes* | OAuth2 client ID | `123456789-abc...` |
| `GMAIL_CLIENT_SECRET` | Yes* | OAuth2 client secret | `GOCSPX-abc...` |
| `AGENT_WEBHOOK_URL` | No | Webhook URL for processed emails | `https://...` |
| `GMAIL_REPLY_EMAIL` | No | Email for replies | `reachus.sherlox@gmail.com` |
| `GMAIL_POLL_INTERVAL` | No | Polling interval (seconds) | `60` |

*Either access token OR refresh token + client credentials

## Troubleshooting

### Deployment Issues

**Problem:** Agent import fails
- **Solution:** Check YAML syntax and ensure all required fields are present

**Problem:** Tools not loading
- **Solution:** 
  - Verify Python file syntax
  - Check all imports are available
  - Ensure tool decorators are correct
  - Verify YAML matches tool names

**Problem:** Environment variables not working
- **Solution:**
  - Verify variables are set in Orchestrate environment
  - Check variable names match exactly (case-sensitive)
  - Ensure variables are available to agent runtime

### Runtime Issues

**Problem:** Gmail API authentication fails
- **Solution:**
  - Check access token is valid and not expired
  - Verify OAuth2 credentials are correct
  - Ensure Gmail API is enabled in Google Cloud Console
  - Check OAuth consent screen is configured

**Problem:** Emails not being processed
- **Solution:**
  - Verify `GMAIL_WATCH_EMAIL` is correct
  - Check Gmail account has proper permissions
  - Verify Gmail API scopes include `gmail.readonly`
  - Check if emails are being filtered/spam

**Problem:** Webhook not receiving payloads
- **Solution:**
  - Verify webhook URL is correct and accessible
  - Check network connectivity from Orchestrate
  - Verify payload format matches expected schema
  - Review webhook response codes

## Security Best Practices

1. **Store Secrets Securely**
   - Use IBM Cloud Secrets Manager for sensitive values
   - Never commit tokens or secrets to version control
   - Rotate access tokens regularly

2. **Use OAuth2 Refresh Tokens**
   - Prefer refresh tokens over access tokens for production
   - Refresh tokens don't expire (unless revoked)
   - Enable automatic token refresh

3. **Restrict API Scopes**
   - Use minimum required Gmail API scopes
   - Review OAuth consent screen permissions

4. **Monitor Access**
   - Enable logging and monitoring
   - Set up alerts for authentication failures
   - Review access logs regularly

## Maintenance

### Updating the Agent

1. Make changes to `email_processor.py` or `email_processor.yaml`
2. Re-upload files via UI or CLI
3. Redeploy the agent
4. Test changes thoroughly

### Updating Environment Variables

```bash
orchestrate agents update \
  --name email_processor \
  --env VARIABLE_NAME=new_value
```

### Monitoring

- Set up alerts for:
  - Gmail API authentication failures
  - Email processing failures
  - Webhook delivery failures
  - Agent downtime

## Additional Resources

- IBM Watsonx Orchestrate Documentation: https://www.ibm.com/docs/en/watsonx-orchestrate
- Gmail API Documentation: https://developers.google.com/gmail/api
- IBM Cloud Secrets Manager: https://cloud.ibm.com/docs/secrets-manager

