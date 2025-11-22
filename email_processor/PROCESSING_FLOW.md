# Email Processing Flow Documentation

This document explains in detail how the Email Processor Agent processes emails from Gmail.

## Overview

The Email Processor Agent monitors a Gmail inbox (`reachus.sherlox@gmail.com`), extracts customer information from incoming emails, determines priority, and sends structured payloads to another agent for further processing.

## Architecture

```
┌─────────────────┐
│   Gmail Inbox   │
│ contactus.@gmail│
└────────┬────────┘
         │
         │ New Email
         ▼
┌─────────────────┐
│  gmail_watcher  │ ◄─── Polls every 60 seconds (configurable)
│      .py        │
└────────┬────────┘
         │
         │ Fetch Email Content
         ▼
┌─────────────────┐
│email_processor  │
│      .py       │
│                 │
│  - process_email│
│  - send_to_agent│
│  - process_and_ │
│    send_email   │
└────────┬────────┘
         │
         │ Structured Payload
         ▼
┌─────────────────┐
│  Agent Webhook  │
│  (or Manual)    │
└─────────────────┘
```

## Processing Flow - Step by Step

### Step 1: Email Detection

**Location**: `gmail_watcher.py` → `_process_new_emails()`

1. **Query Gmail API** for unread emails:
   ```python
   query = f'to:{GMAIL_WATCH_EMAIL} is:unread'
   ```

2. **Fetch message IDs** of matching emails (up to 50 at a time)

3. **Check processed emails**:
   - Load `processed_emails.json` to get list of already processed email IDs
   - Filter out already processed emails to avoid duplicates

4. **For each new email**:
   - Fetch full email content from Gmail API
   - Parse email headers and body

### Step 2: Email Parsing

**Location**: `gmail_watcher.py` → `_parse_email_message()`

1. **Extract Headers**:
   - `From`: Sender's email address and name
   - `To`: Recipient email address
   - `Subject`: Email subject line

2. **Extract Body**:
   - Decode base64-encoded email body
   - Handle multipart emails (text/plain and text/html)
   - Extract text content from all parts
   - Handle encoding issues gracefully

3. **Return Structured Data**:
   ```python
   {
       'from': 'customer@example.com',
       'to': 'reachus.sherlox@gmail.com',
       'subject': 'Need help with refund',
       'body': 'Full email text content...',
       'message_id': 'abc123',
       'thread_id': 'xyz789'
   }
   ```

### Step 3: Information Extraction

**Location**: `email_processor.py` → `process_email()`

The agent extracts the following information using various heuristics:

#### 3.1 Customer Email Extraction

**Function**: `_extract_email_address()`

1. **From Header** (Primary):
   - Parse "From" header using `email.utils.parseaddr()`
   - Extract email address from format: `"Name" <email@example.com>`

2. **Email Body** (Fallback):
   - Search for email patterns: `[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}`
   - Use first valid email found in body

3. **Default**: `"unknown@example.com"` if no email found

#### 3.2 Customer Name Extraction

**Function**: `_extract_name()`

Tries multiple strategies in order:

1. **From Header**:
   - Extract name from "From" header: `"John Doe" <john@example.com>`

2. **Explicit Patterns**:
   - `"I am John Doe"` or `"I'm John Doe"`
   - Pattern: `\bI(?:'m| am) ([A-Z][A-Za-z\s'`\-\.]{1,60})`

3. **Signature Lines**:
   - Look for names after signature markers:
   - Pattern: `(?:Regards|Best|Thanks|Sincerely)[\,\s]*\n\s*([A-Z][A-Za-z\s\-\.]{1,60})`

4. **Beginning of Email**:
   - Check first 5 lines for name-like patterns
   - Must start with capital letter, 2-60 characters
   - Pattern: `^[A-Z][A-Za-z\s\'\-\.]{1,60}$`

5. **Default**: `"Unknown"` if no name found

#### 3.3 Phone Number Extraction

**Function**: `_extract_phone_number()`

1. **Search Pattern**:
   - Pattern: `\+?\d[\d\s\-\(\)]{6,}\d`
   - Supports formats:
     - `+1-555-123-4567`
     - `(555) 123-4567`
     - `555-1234`
     - `+91 98765 43210`

2. **Cleanup**:
   - Strip whitespace
   - Return first valid phone number found

3. **Default**: Empty string `""` if no phone found

#### 3.4 Issue Description Extraction

**Function**: `_extract_issue_description()`

Removes noise and extracts the core message:

1. **Remove Greetings**:
   - Lines starting with: `hi`, `hello`, `dear`, `good morning`, etc.

2. **Remove Signature Markers**:
   - Stop at: `regards`, `best`, `thanks`, `sincerely`, `yours`

3. **Remove Contact Info**:
   - Lines containing email addresses
   - Lines containing phone numbers
   - Lines with "I am" introductions

4. **Remove Email Headers**:
   - Lines starting with: `from:`, `to:`, `subject:`, `sent:`, `date:`

5. **Join Remaining Lines**:
   - Combine all remaining lines into issue description
   - Fallback to full email text if too much was removed

#### 3.5 Priority Determination

**Function**: `_determine_priority()`

Analyzes email content for keywords:

1. **HIGH Priority** (if any keyword found):
   - `urgent`, `emergency`, `critical`, `asap`, `immediately`
   - `refund`, `cancel`, `cancelled`, `complaint`, `issue`
   - `problem`, `error`, `broken`, `not working`, `failed`

2. **LOW Priority** (if found and no HIGH keywords):
   - `question`, `inquiry`, `info`, `information`, `general`
   - `feedback`, `suggestion`

3. **MEDIUM Priority** (default):
   - All other emails

**Note**: Priority is determined from both subject and body text combined.

### Step 4: Payload Creation

**Location**: `email_processor.py` → `process_email()`

Creates structured payload in required format:

```json
{
    "CustomerName": "John Doe",
    "CustomerEmail": "john@example.com",
    "CustomerPhoneNumber": "+1-555-123-4567",
    "IssueDescription": "I need a refund for my cancelled booking",
    "Priority": "HIGH"
}
```

**Field Details**:
- `CustomerName`: Extracted name or `"Unknown"`
- `CustomerEmail`: Extracted email or `"unknown@example.com"`
- `CustomerPhoneNumber`: Extracted phone or `""` (empty string)
- `IssueDescription`: Cleaned email body text
- `Priority`: `"HIGH"`, `"MEDIUM"`, or `"LOW"`

### Step 5: Validation and Reply Logic

**Location**: `email_processor.py` → `process_and_send_email()`

Before sending to agent, the system validates the email:

1. **Check if Complaint/Error**:
   - Function: `_is_complaint_or_error()`
   - Looks for keywords: complaint, issue, problem, error, refund, cancel, etc.
   - Checks if issue description is substantial (>50 characters)

2. **Check Required Information**:
   - Function: `_has_required_information()`
   - Validates:
     - Customer email is valid (not "unknown@example.com")
     - Customer name is valid (not "Unknown")
     - Issue description is substantial (>20 characters)

3. **If Invalid or Missing Info**:
   - Sends reply email from `GMAIL_REPLY_EMAIL` (default: `reachus.sherlox@gmail.com`)
   - Requests missing information
   - Explains what's needed
   - Email is marked as processed (no duplicate replies)

4. **If Valid Complaint with Required Info**:
   - Proceeds to Step 6 (Sending to Agent)

### Step 6: Sending to Agent

**Location**: `email_processor.py` → `send_to_agent()`

1. **Validate Payload**:
   - Check payload is a dictionary
   - Verify required fields: `CustomerName`, `CustomerEmail`, `IssueDescription`, `Priority`

2. **Send via Webhook** (if `AGENT_WEBHOOK_URL` is set):
   ```python
   POST https://your-webhook-url.com/api/process
   Content-Type: application/json
   
   {
       "CustomerName": "...",
       "CustomerEmail": "...",
       ...
   }
   ```

3. **Handle Response**:
   - Success (200-299): Mark as sent successfully
   - Error (400+): Log error and return error status
   - Network Error: Catch exception and return error

4. **Fallback** (if no webhook configured):
   - Save payload to `saved_payloads.json` file
   - File location: `email_processor/saved_payloads.json`
   - Format: JSON array with timestamp and payload
   - Allows manual processing later

### Step 6: Mark as Processed

**Location**: `gmail_watcher.py` → `_save_processed_email()`

1. **Save Email ID**:
   - Add email message ID to `processed_emails.json`
   - Prevents duplicate processing

2. **File Format**:
   ```json
   {
       "processed_ids": ["msg_id_1", "msg_id_2", ...]
   }
   ```

## Complete Processing Example

### Input Email

```
From: John Doe <john@example.com>
To: reachus.sherlox@gmail.com
Subject: URGENT: Need refund for cancelled booking

Hello,

I am John Doe and I need an urgent refund for my cancelled booking.
My phone number is +1-555-123-4567.

Please process this as soon as possible.

Thanks,
John
```

### Processing Steps

1. **Email Detection**: Gmail watcher finds unread email
2. **Parsing**: Extracts headers and body
3. **Extraction**:
   - Name: "John Doe" (from "I am John Doe")
   - Email: "john@example.com" (from From header)
   - Phone: "+1-555-123-4567" (from body)
   - Issue: "I need an urgent refund for my cancelled booking. Please process this as soon as possible."
   - Priority: HIGH (keywords: "urgent", "refund", "cancelled")

4. **Payload Creation**:
   ```json
   {
       "CustomerName": "John Doe",
       "CustomerEmail": "john@example.com",
       "CustomerPhoneNumber": "+1-555-123-4567",
       "IssueDescription": "I need an urgent refund for my cancelled booking. Please process this as soon as possible.",
       "Priority": "HIGH"
   }
   ```

5. **Sending**: POST to `AGENT_WEBHOOK_URL`
6. **Mark Processed**: Save email ID to prevent reprocessing

## Error Handling

### Gmail API Errors

- **401 Unauthorized**: Token expired or invalid
  - Solution: Refresh token or get new access token
- **403 Forbidden**: Insufficient permissions
  - Solution: Check OAuth2 scopes
- **429 Too Many Requests**: Rate limit exceeded
  - Solution: Increase `GMAIL_POLL_INTERVAL`

### Processing Errors

- **Missing Information**: Uses defaults (Unknown, empty string)
- **Invalid Email Format**: Falls back to body extraction
- **Webhook Failure**: Logs error, email still marked as processed

### Retry Logic

- **Email Processing**: No automatic retry (marked as processed to avoid loops)
- **Webhook Sending**: No automatic retry (can be added if needed)
- **Token Refresh**: Automatic refresh if refresh token is configured

## Performance Considerations

1. **Polling Interval**: 
   - Default: 60 seconds
   - Minimum recommended: 10 seconds (to avoid rate limiting)
   - Adjust based on email volume

2. **Batch Processing**:
   - Processes up to 50 emails per poll
   - Processes emails sequentially (one at a time)

3. **Memory Usage**:
   - `processed_emails.json` grows over time
   - Consider periodic cleanup of old email IDs

4. **API Rate Limits**:
   - Gmail API: 1 billion quota units per day
   - Each message fetch: ~5 quota units
   - Each message list: ~1 quota unit

## Monitoring and Logging

### Log Messages

- `"Starting Gmail watcher for {email}"`: Watcher started
- `"Found {N} new email(s) to process"`: New emails detected
- `"Successfully processed email {id}"`: Email processed successfully
- `"Failed to process email {id}: {error}"`: Processing failed
- `"Error refreshing token: {error}"`: Token refresh failed

### Key Metrics to Monitor

1. **Emails Processed**: Count of successfully processed emails
2. **Processing Errors**: Count of failed processing attempts
3. **Webhook Failures**: Count of failed webhook sends
4. **Token Refresh Failures**: Count of authentication errors
5. **Processing Time**: Time taken to process each email

## Integration Points

### With IBM Watsonx Orchestrate

The agent can be triggered:
1. **Automatically**: Via `gmail_watcher.py` polling
2. **Manually**: Via Orchestrate agent interface
3. **Via API**: Call agent tools directly

### With Other Agents

The processed payload can be sent to:
1. **Webhook URL**: HTTP POST to configured endpoint
2. **Another Orchestrate Agent**: Via agent collaboration
3. **API Endpoint**: Any REST API that accepts JSON

## Customization

### Adjusting Priority Keywords

Edit `_determine_priority()` in `email_processor.py`:
```python
high_priority_keywords = [
    'urgent', 'emergency', 'your-custom-keyword'
]
```

### Adjusting Extraction Patterns

Edit extraction functions in `email_processor.py`:
- `_extract_name()`: Modify name patterns
- `_extract_phone_number()`: Modify phone regex
- `_extract_issue_description()`: Modify cleanup rules

### Adjusting Polling Behavior

Edit `gmail_watcher.py`:
- Change `POLL_INTERVAL` environment variable
- Modify `max_results` in `_list_messages()` (default: 50)
- Adjust query in `_process_new_emails()`

