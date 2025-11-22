# Setup Without Google Cloud Console Access

This guide explains how to set up the Email Processor Agent if you **don't have access to Google Cloud Console**.

## Understanding the Requirements

The Gmail API requires OAuth2 credentials that are typically created in Google Cloud Console. However, there are several alternatives if you don't have access:

## Option 1: Use Existing Credentials (Recommended)

If someone else has already set up the Gmail API credentials, you can use their credentials:

### Step 1: Get the Credentials File

Ask someone with Google Cloud Console access to:
1. Download their `credentials.json` file
2. Share it with you (securely - this file contains sensitive information!)

### Step 2: Get Authentication Tokens

You have two options:

#### Option A: Use Pre-generated Tokens

If they've already run `setup_gmail_auth.py`, ask them to share:
- The **refresh token** (from the script output or `token.pickle` file)
- The **client ID** and **client secret** (from `credentials.json`)

Then set these environment variables:
```powershell
# Windows PowerShell
$env:GMAIL_REFRESH_TOKEN="1//0g..."
$env:GMAIL_CLIENT_ID="123456789-abc.apps.googleusercontent.com"
$env:GMAIL_CLIENT_SECRET="GOCSPX-abc..."
$env:GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
```

#### Option B: Generate Your Own Tokens

1. Place the shared `credentials.json` file in the `email_processor/` directory
2. Run the authentication script:
   ```bash
   python setup_gmail_auth.py
   ```
3. This will open a browser for you to authorize the application
4. Copy the tokens from the output and set them as environment variables

### Step 3: Set Environment Variables

```powershell
# Windows PowerShell
$env:GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
$env:GMAIL_REFRESH_TOKEN="1//0g..."  # From setup_gmail_auth.py
$env:GMAIL_CLIENT_ID="123456789-abc.apps.googleusercontent.com"  # From credentials.json
$env:GMAIL_CLIENT_SECRET="GOCSPX-abc..."  # From credentials.json
$env:GMAIL_REPLY_EMAIL="reachus.sherlox@gmail.com"  # Optional
$env:GMAIL_POLL_INTERVAL="60"
```

## Option 2: Request Google Cloud Console Access

If you're working in an organization:

1. **Contact your IT/Admin team** to request:
   - Access to Google Cloud Console
   - Permission to create OAuth2 credentials
   - Access to the existing project (if one exists)

2. **If you have a Google Workspace account**, your admin can:
   - Grant you access to the Google Cloud project
   - Or create credentials on your behalf

3. **For personal Gmail accounts**, you can:
   - Create a free Google Cloud account at https://console.cloud.google.com/
   - Free tier includes $300 credit and doesn't require payment for basic API usage

## Option 3: Use Access Token Directly (Short-term Solution)

If someone can generate an access token for you:

```powershell
# Windows PowerShell
$env:GMAIL_ACCESS_TOKEN="ya29.a0AfH6SMBx..."
$env:GMAIL_WATCH_EMAIL="reachus.sherlox@gmail.com"
```

**⚠️ Important Limitations:**
- Access tokens expire after ~1 hour
- You'll need to get a new token periodically
- Not suitable for long-term/production use
- Better to use refresh tokens (Option 1)

## Option 4: Alternative Email Providers (Requires Code Changes)

If you cannot use Gmail API at all, you could modify the code to use:

1. **IMAP** - Works with Gmail and other email providers
   - Requires App Passwords (for Gmail)
   - No Google Cloud Console needed
   - Would require significant code changes

2. **Other Email APIs** - Such as:
   - Microsoft Graph API (for Outlook)
   - SendGrid API
   - Mailgun API

**Note:** This would require rewriting parts of `gmail_watcher.py` and `email_processor.py`.

## Security Considerations

⚠️ **Important Security Notes:**

1. **Never commit credentials to version control**
   - Add `credentials.json` and `token.pickle` to `.gitignore`
   - Never share credentials publicly

2. **Share credentials securely**
   - Use encrypted channels (e.g., password-protected zip, secure file sharing)
   - Don't send via email or chat without encryption

3. **Rotate credentials if compromised**
   - If credentials are exposed, revoke them in Google Cloud Console
   - Generate new credentials

4. **Limit access**
   - Only share with trusted team members
   - Use the minimum required scopes

## Quick Setup Checklist (Using Shared Credentials)

- [ ] Obtain `credentials.json` from someone with Google Cloud Console access
- [ ] Place `credentials.json` in `email_processor/` directory
- [ ] Run `python setup_gmail_auth.py` to generate tokens
- [ ] Set environment variables (GMAIL_REFRESH_TOKEN, GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET)
- [ ] Set `GMAIL_WATCH_EMAIL` environment variable
- [ ] Test with `python gmail_watcher.py`

## Troubleshooting

### "credentials.json not found"
- Make sure the file is in the `email_processor/` directory
- Check the file name is exactly `credentials.json` (case-sensitive on Linux/Mac)

### "Access blocked: Email processor has not completed the Google verification process"
- **This is the most common error!** It means your email hasn't been added as a test user
- Ask the person who created the credentials to:
  1. Go to Google Cloud Console → "APIs & Services" → "OAuth consent screen"
  2. Scroll to "Test users" section
  3. Click "+ ADD USERS"
  4. Add your Gmail email address (the one you're using to authenticate)
  5. Wait 1-2 minutes for changes to take effect
- Then delete `token.pickle` (if it exists) and re-run `python setup_gmail_auth.py`

### "403 Forbidden" or "Insufficient permissions"
- The OAuth consent screen may need your email added as a test user
- Ask the person who created the credentials to add your email to test users
- Or request the app to be published (for production use)

### "Invalid grant" when refreshing token
- The refresh token may have been revoked
- Re-run `setup_gmail_auth.py` to get a new refresh token

### "Access denied" during OAuth flow
- Make sure you're using the correct Gmail account
- Check that the OAuth consent screen allows your account
- Verify the credentials are for the correct project

## Getting Help

If you need help:
1. Contact your team member who has Google Cloud Console access
2. Request access to Google Cloud Console from your organization
3. Consider creating a free personal Google Cloud account for testing

## Next Steps

Once you have credentials set up:
1. Follow the main [LOCAL_SETUP.md](./LOCAL_SETUP.md) guide from Step 4 onwards
2. Test the connection with a sample email
3. Configure webhook URL if needed
4. Set up for production deployment

