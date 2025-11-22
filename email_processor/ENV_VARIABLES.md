# Environment Variables for Email Processor

This document provides detailed information about all environment variables required for the Email Processor Agent.

## Required Environment Variables

### Gmail API Authentication

#### Option 1: Using Access Token (Simpler, but tokens expire)
```bash
GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."
```
- **Description**: Direct Gmail API access token
- **How to get**: Run `python setup_gmail_auth.py` and copy the token from output
- **Expiration**: Access tokens typically expire after 1 hour
- **When to use**: For testing or short-term use
- **Example**: `GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."`

#### Option 2: Using OAuth2 Refresh Token (Recommended for Production)
```bash
GMAIL_REFRESH_TOKEN="1//0g..."
GMAIL_CLIENT_ID="123456789-abc.apps.googleusercontent.com"
GMAIL_CLIENT_SECRET="GOCSPX-abc..."
```
- **Description**: OAuth2 credentials that allow automatic token refresh
- **How to get**: 
  1. Run `python setup_gmail_auth.py`
  2. Copy the refresh token, client ID, and client secret from the output
  3. Or download from Google Cloud Console → APIs & Services → Credentials
- **Expiration**: Refresh tokens don't expire (unless revoked)
- **When to use**: For production deployments
- **Example**:
  ```bash
  GMAIL_REFRESH_TOKEN="1//0g..."
  GMAIL_CLIENT_ID="123456789-abc.apps.googleusercontent.com"
  GMAIL_CLIENT_SECRET="GOCSPX-abc..."
  ```

### Gmail Configuration

```bash
GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
```
- **Description**: The Gmail address to monitor for incoming emails
- **Default**: `reachus.sherlox@gmail.com`
- **Required**: Yes
- **Example**: `GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"`

```bash
GMAIL_REPLY_EMAIL="reachus.sherlox@gmail.com"
```
- **Description**: The Gmail address to send reply emails from
- **Default**: `reachus.sherlox@gmail.com`
- **Required**: No (only needed if you want to send reply emails)
- **Note**: The authenticated Gmail account must have permission to send from this address
- **Example**: `GMAIL_REPLY_EMAIL="reachus.sherlox@gmail.com"`

### Agent Integration

```bash
AGENT_WEBHOOK_URL="https://your-agent-webhook-url.com/api/process"
```
- **Description**: Webhook URL where processed email payloads will be sent
- **Default**: Empty string (no webhook configured)
- **Required**: No (but recommended for automatic processing)
- **Format**: Full HTTP/HTTPS URL
- **Example**: `AGENT_WEBHOOK_URL="https://api.example.com/webhook/process"`

### Optional Configuration

```bash
GMAIL_POLL_INTERVAL="60"
```
- **Description**: How often (in seconds) to check for new emails
- **Default**: `60` (1 minute)
- **Required**: No
- **Minimum**: `10` (recommended to avoid rate limiting)
- **Example**: `GMAIL_POLL_INTERVAL="30"` (check every 30 seconds)

```bash
GMAIL_API_BASE="https://gmail.googleapis.com/gmail/v1"
```
- **Description**: Base URL for Gmail API (usually don't need to change)
- **Default**: `https://gmail.googleapis.com/gmail/v1`
- **Required**: No
- **When to change**: Only if using a custom Gmail API endpoint

## Setting Environment Variables

### Windows (PowerShell)
```powershell
$env:GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
$env:GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."
$env:AGENT_WEBHOOK_URL="https://your-webhook-url.com/api/process"
$env:GMAIL_POLL_INTERVAL="60"
```

### Windows (Command Prompt)
```cmd
set GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
set GMAIL_ACCESS_TOKEN=ya29.a0AfH6SMBx...
set AGENT_WEBHOOK_URL=https://your-webhook-url.com/api/process
set GMAIL_POLL_INTERVAL=60
```

### Linux/Mac (Bash)
```bash
export GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
export GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."
export AGENT_WEBHOOK_URL="https://your-webhook-url.com/api/process"
export GMAIL_POLL_INTERVAL="60"
```

### Using .env File (Recommended)
Create a `.env` file in the `email_processor` directory:
```bash
GMAIL_WATCH_EMAIL=reachus.sherlox@gmail.com
GMAIL_ACCESS_TOKEN=ya29.a0AfH6SMBx...
GMAIL_REFRESH_TOKEN=1//0g...
GMAIL_CLIENT_ID=123456789-abc.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-abc...
AGENT_WEBHOOK_URL=https://your-webhook-url.com/api/process
GMAIL_POLL_INTERVAL=60
```

**Note**: If using a `.env` file, you'll need to load it in your code using `python-dotenv`:
```python
from dotenv import load_dotenv
load_dotenv()
```

### IBM Watsonx Orchestrate Environment Variables
When deploying to IBM Watsonx Orchestrate, set these in the agent's environment configuration:
1. Go to your agent settings
2. Navigate to "Environment Variables" or "Configuration"
3. Add each variable with its value
4. Mark sensitive variables (tokens, secrets) as "Secret" or "Encrypted"

## Environment Variable Priority

The system checks for authentication in this order:
1. `GMAIL_ACCESS_TOKEN` (if set, used directly)
2. `GMAIL_REFRESH_TOKEN` + `GMAIL_CLIENT_ID` + `GMAIL_CLIENT_SECRET` (if access token not set, refresh token is used to get a new access token)

## Security Best Practices

1. **Never commit credentials to version control**
   - Add `.env` to `.gitignore`
   - Never commit `token.pickle` or `credentials.json`

2. **Use environment variables, not hardcoded values**
   - Store sensitive data in environment variables
   - Use secret management services in production

3. **Rotate tokens regularly**
   - Refresh tokens should be rotated periodically
   - Revoke old tokens when generating new ones

4. **Use minimal scopes**
   - Only request Gmail API scopes you actually need
   - Current scopes: `gmail.readonly` and `gmail.modify`

5. **Restrict access**
   - Limit who can access the Gmail account
   - Use service accounts for production when possible

## Troubleshooting

### "Gmail access token not available"
- **Cause**: Missing or invalid `GMAIL_ACCESS_TOKEN` or OAuth2 credentials
- **Solution**: 
  1. Run `python setup_gmail_auth.py` to get tokens
  2. Set `GMAIL_ACCESS_TOKEN` or configure OAuth2 credentials
  3. Verify tokens are not expired

### "Failed to refresh token"
- **Cause**: Invalid refresh token or client credentials
- **Solution**:
  1. Verify `GMAIL_REFRESH_TOKEN`, `GMAIL_CLIENT_ID`, and `GMAIL_CLIENT_SECRET` are correct
  2. Check if refresh token was revoked in Google Cloud Console
  3. Re-run `setup_gmail_auth.py` to get new tokens

### "Webhook URL not configured"
- **Cause**: `AGENT_WEBHOOK_URL` is not set
- **Solution**: Set `AGENT_WEBHOOK_URL` to your webhook endpoint, or process emails manually

### "Email address not found"
- **Cause**: `GMAIL_WATCH_EMAIL` is incorrect or not accessible
- **Solution**: Verify the email address is correct and the authenticated account has access to it

## Quick Setup Checklist

- [ ] Gmail API enabled in Google Cloud Console
- [ ] OAuth2 credentials created and downloaded
- [ ] `credentials.json` placed in `email_processor/` directory
- [ ] `python setup_gmail_auth.py` run successfully
- [ ] `GMAIL_ACCESS_TOKEN` or OAuth2 credentials set
- [ ] `GMAIL_WATCH_EMAIL` set to correct email address
- [ ] `AGENT_WEBHOOK_URL` set (if using webhook integration)
- [ ] `GMAIL_POLL_INTERVAL` set (optional, defaults to 60)
- [ ] Environment variables tested and working

## Example Complete Configuration

```bash
# Gmail API Authentication (Option 1: Direct Token)
GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."

# OR (Option 2: OAuth2 - Recommended)
GMAIL_REFRESH_TOKEN="1//0g..."
GMAIL_CLIENT_ID="123456789-abc.apps.googleusercontent.com"
GMAIL_CLIENT_SECRET="GOCSPX-abc..."

# Gmail Configuration
GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
GMAIL_REPLY_EMAIL="reachus.sherlox@gmail.com"

# Agent Integration
AGENT_WEBHOOK_URL="https://api.example.com/webhook/process"

# Optional
GMAIL_POLL_INTERVAL="60"
```

