# Email Sender

This module sends emails using the Gmail API with OAuth2 authentication.

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Get Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Gmail API" and click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure the OAuth consent screen first:
     - Choose "External" (unless you have a Google Workspace)
     - Fill in the required fields (App name, User support email, etc.)
     - Add your email to "Test users" if in testing mode
   - Choose "Desktop app" as the application type
   - Click "Create"
   - Download the credentials JSON file
5. Save the downloaded file as `credentials.json` in this directory

### Step 3: Run the Setup Script

```bash
python setup_gmail_auth.py
```

This will:
- Open a browser window for you to authorize the application
- Save your authentication token to `token.pickle`
- Allow you to send emails using the Gmail API

**Note:** Make sure you're logged into the Gmail account you want to use for sending emails when the browser opens.

### Step 4: Run the Email Sender

**Important:** The recipient email must match the customer email from greeter_agent POST call.

You can run the email sender in two ways:

#### Option 1: Using Command Line Arguments

```bash
python email_sender.py --recipient customer@example.com --subject "Your Subject" --body "Your message"
```

#### Option 2: Using Environment Variables

```bash
# Set the customer email (must match greeter_agent customer email)
export CUSTOMER_EMAIL=customer@example.com
export SENDER_EMAIL=your_email@gmail.com
export EMAIL_SUBJECT="Your Subject"
export EMAIL_BODY="Your message"

python email_sender.py
```

**On Windows PowerShell:**
```powershell
$env:CUSTOMER_EMAIL="customer@example.com"
$env:SENDER_EMAIL="your_email@gmail.com"
$env:EMAIL_SUBJECT="Your Subject"
$env:EMAIL_BODY="Your message"
python email_sender.py
```

The script will:
- Load your saved authentication token
- Validate that recipient email is provided
- Send the email to the specified recipient (must match customer email from greeter_agent)

## Command Line Options

```bash
python email_sender.py --help
```

Available options:
- `--recipient` or `-r`: Recipient email address (required, must match customer email from greeter_agent)
- `--sender` or `-s`: Sender email address (defaults to environment variable SENDER_EMAIL or "your_email@gmail.com")
- `--subject`: Email subject (defaults to environment variable EMAIL_SUBJECT or "Gmail API OAuth Test")
- `--body`: Email body text (defaults to environment variable EMAIL_BODY or default test message)

## Integration with Greeter Agent

**Important Requirement:** The recipient email in this script must be the same as the customer email coming via greeter_agent POST call.

When greeter_agent receives a POST request with customer information, it includes a `CustomerEmail` field. This same email address should be used as the recipient when calling this email sender script.

Example workflow:
1. Greeter agent receives POST with: `{"CustomerEmail": "customer@example.com", ...}`
2. Use the same email when calling email_sender:
   ```bash
   python email_sender.py --recipient customer@example.com
   ```

## Troubleshooting

### "Recipient email is required!"
- Make sure you provide the recipient email via command line (`--recipient` or `-r`) or environment variable (`CUSTOMER_EMAIL`)
- The recipient email must match the customer email from greeter_agent POST call

### "credentials.json not found"
- Make sure you've downloaded the OAuth2 credentials from Google Cloud Console
- Save the file as `credentials.json` in the `email_sender` directory

### "Access blocked: This app's request is invalid"
- Make sure you've enabled the Gmail API in Google Cloud Console
- Check that your OAuth consent screen is configured
- If in testing mode, make sure your email is added to "Test users"

### "Token expired" or "Invalid credentials"
- Delete `token.pickle` and run `setup_gmail_auth.py` again
- Make sure your credentials.json file is valid

### "Permission denied" or "Insufficient permissions"
- Make sure the Gmail API scope `gmail.send` is enabled
- Re-authenticate by running `setup_gmail_auth.py` again

## Files

- `email_sender.py` - Main script for sending emails
- `setup_gmail_auth.py` - Setup script for Gmail authentication
- `credentials.json` - OAuth2 credentials from Google Cloud Console (you need to download this)
- `token.pickle` - Saved authentication token (created after running setup)

## Security Notes

- **Never commit `credentials.json` or `token.pickle` to version control**
- Add these files to `.gitignore`:
  ```
  credentials.json
  token.pickle
  ```
- Keep your credentials secure and don't share them

