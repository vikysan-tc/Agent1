# EmailJS Setup Guide

This guide will help you set up EmailJS so that the ResolvX landing page can automatically send emails to `reachus.sherlox@gmail.com` without opening an email client.

## Step 1: Create EmailJS Account

1. Go to [https://www.emailjs.com/](https://www.emailjs.com/)
2. Click "Sign Up" and create a free account
3. The free plan allows 200 emails per month, which is perfect for getting started

## Step 2: Add Email Service

1. In your EmailJS dashboard, go to **"Email Services"**
2. Click **"Add New Service"**
3. Choose your email provider:
   - **Gmail** (Recommended) - Connect your Gmail account
   - **Outlook** - Connect your Outlook account
   - **Other** - Use SMTP settings
4. Follow the setup instructions to connect your email account
5. **Important**: Use the email account that will SEND the emails (not the recipient)
6. After connecting, note down your **Service ID** (e.g., `service_xxxxxxx`)

## Step 3: Create Email Template

1. Go to **"Email Templates"** in the EmailJS dashboard
2. Click **"Create New Template"**
3. Use the following settings:

   **Template Name**: `ResolvX Complaint Form`

   **To Email**: `reachus.sherlox@gmail.com`

   **From Name**: `{{from_name}}`

   **From Email**: `{{from_email}}`

   **Reply To**: `{{from_email}}`

   **Subject**: `{{subject}}`

   **Content** (HTML or Plain Text):
   ```
   Dear ResolvX Team,

   A new complaint has been submitted through the ResolvX platform.

   Customer Information:
   - Name: {{customer_name}}
   - Email: {{customer_email}}
   - Phone: {{phone_number}}

   Company: {{company_name}}

   Subject: {{subject}}

   Message:
   {{message}}

   ---
   This email was sent automatically from the ResolvX complaint form.
   ```

4. Click **"Save"**
5. Note down your **Template ID** (e.g., `template_xxxxxxx`)

## Step 4: Get Your Public Key

1. Go to **"Account"** → **"General"** in the EmailJS dashboard
2. Find your **Public Key** (also called API Key)
3. Copy it (e.g., `xxxxxxxxxxxxxxxxxx`)

## Step 5: Update script.js

1. Open `resolvx_landing/script.js`
2. Find these lines near the top:
   ```javascript
   const EMAILJS_SERVICE_ID = 'YOUR_SERVICE_ID';
   const EMAILJS_TEMPLATE_ID = 'YOUR_TEMPLATE_ID';
   const EMAILJS_PUBLIC_KEY = 'YOUR_PUBLIC_KEY';
   ```
3. Replace them with your actual credentials:
   ```javascript
   const EMAILJS_SERVICE_ID = 'service_xxxxxxx';      // Your Service ID from Step 2
   const EMAILJS_TEMPLATE_ID = 'template_xxxxxxx';    // Your Template ID from Step 3
   const EMAILJS_PUBLIC_KEY = 'xxxxxxxxxxxxxxxxxx';   // Your Public Key from Step 4
   ```
4. Save the file

## Step 6: Test the Form

1. Open `index.html` in your browser (or use a local server)
2. Fill out the complaint form
3. Click "Submit Complaint"
4. The email should be sent automatically to `reachus.sherlox@gmail.com`
5. Check the EmailJS dashboard → "Logs" to see if the email was sent successfully

## Troubleshooting

### Email not sending?
- Check the browser console (F12) for error messages
- Verify all three credentials are correct in `script.js`
- Check EmailJS dashboard → "Logs" for error details
- Make sure you haven't exceeded the free plan limit (200 emails/month)

### Template variables not working?
- Make sure the variable names in your template match exactly:
  - `{{from_name}}`
  - `{{from_email}}`
  - `{{subject}}`
  - `{{message}}`
  - `{{company_name}}`
  - `{{phone_number}}`
  - `{{customer_name}}`
  - `{{customer_email}}`

### Still having issues?
- Check EmailJS documentation: [https://www.emailjs.com/docs/](https://www.emailjs.com/docs/)
- Make sure your email service is properly connected
- Verify the "To Email" in your template is set to `reachus.sherlox@gmail.com`

## Security Note

The Public Key is safe to use in frontend code - it's designed to be public. However, make sure:
- You don't share your Service ID and Template ID publicly
- You monitor your EmailJS account for unusual activity
- You set up rate limiting if needed

## Alternative: Using Your Own Backend

If you prefer not to use EmailJS, you can:
1. Create a backend API endpoint (Node.js, Python, etc.)
2. Update `sendEmailDirectly()` function to call your API
3. Handle email sending on the server side

This gives you more control but requires server setup and maintenance.

