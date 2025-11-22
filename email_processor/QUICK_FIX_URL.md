# Quick Fix: URL Format Issue

## Your URL
```
https://api.ca-tor.watson-orchestrate.cloud.ibm.com/instances/7983dce8-73d5-4ac1-b2ad-1d74de2fc994
```

## The Problem
The CLI needs only the **base URL**, not the full instance URL with `/instances/...`.

## The Solution

Use this command with the **base URL only**:

```bash
orchestrate env add --name watsonx-prod --url https://api.ca-tor.watson-orchestrate.cloud.ibm.com --type ibm_iam --activate
```

**Note**: Remove `/instances/7983dce8-73d5-4ac1-b2ad-1d74de2fc994` from the URL.

## Complete Deployment Steps

1. **Install CLI** (if not already installed):
   ```bash
   pip install --upgrade ibm-watsonx-orchestrate
   ```

2. **Configure environment** (use base URL only):
   ```bash
   orchestrate env add --name watsonx-prod --url https://api.ca-tor.watson-orchestrate.cloud.ibm.com --type ibm_iam --activate
   ```
   - You'll be prompted for your IBM Cloud API key
   - The instance ID is automatically detected from your API key

3. **Navigate to email_processor directory**:
   ```bash
   cd email_processor
   ```

4. **Import the agent**:
   ```bash
   orchestrate agents import -f email_processor.yaml
   ```

5. **Deploy the agent**:
   ```bash
   orchestrate agents deploy --name email_processor
   ```

## Common Errors and Fixes

### Error: "Invalid URL format"
- **Cause**: Using full instance URL instead of base URL
- **Fix**: Remove `/instances/...` from the URL

### Error: "Authentication failed"
- **Cause**: Invalid or expired API key
- **Fix**: 
  1. Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
  2. Create a new API key
  3. Use it when prompted

### Error: "Instance not found"
- **Cause**: API key doesn't have access to the instance
- **Fix**: Ensure your IBM Cloud account has access to the Watsonx Orchestrate instance

## Verify Your Setup

```bash
# Check environment is configured
orchestrate env list

# Check agent was created
orchestrate agents list

# Get agent details
orchestrate agents get --name email_processor
```

## Need Help?

If you're still getting errors, share:
1. The exact error message
2. The command you ran
3. Your Python version: `python --version`
4. Your CLI version: `orchestrate --version`

