# CarePilot - the customer's co-pilot Landing Page

A modern, responsive landing page for CarePilot - the customer's co-pilot - AI Customer Complaint Resolver and Analyser.

## Features

- **Beautiful Modern UI**: Clean, professional design with gradient accents
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Complaint Submission Form**: Easy-to-use form to submit customer complaints
- **Email Integration**: Sends complaints directly to the email processor agent

## How It Works

The landing page opens **Gmail** with a pre-filled email to `reachus.sherlox@gmail.com`. When a user submits the form:

1. The form collects all complaint details
2. Validates the input
3. **Opens Gmail in a new window** with the email pre-filled
4. User reviews and sends the email from Gmail
5. The email processor agent receives and processes the complaint

**No setup required!** The page works immediately and opens Gmail for the user to send the complaint.

## Running the Landing Page

### Simple Method (No Server Required)

1. Open `index.html` directly in your web browser
2. The page will work, but email sending will use the mailto fallback

### Using a Local Server (Recommended)

**Important:** The dashboard requires API access. To avoid CORS issues, you need to run a proxy server.

#### Step 1: Start the CORS Proxy Server

Open a terminal and run:
```bash
cd resolvx_landing
python proxy_server.py
```

This will start a proxy server on `http://localhost:8001` that adds CORS headers.

#### Step 2: Start the Landing Page Server

Open another terminal and run:

1. **Using Python:**
   ```bash
   cd resolvx_landing
   python -m http.server 8000
   ```

2. **Using Node.js:**
   ```bash
   cd resolvx_landing
   npx http-server -p 8000
   ```

3. **Using VS Code:**
   - Install "Live Server" extension
   - Right-click on `index.html`
   - Select "Open with Live Server"

#### Step 3: Access the Landing Page

Open: `http://localhost:8000`

**Note:** Keep both servers running (proxy on port 8001, landing page on port 8000) for the dashboard to work.

For more CORS solutions, see [CORS_SETUP.md](CORS_SETUP.md)

## Form Fields

- **Your Email Address** (Required): Customer's email for updates
- **Your Name** (Required): Customer's full name
- **Company Name** (Required): The company the complaint is against
- **Phone Number** (Optional): Customer's contact number
- **Problem Description** (Required): Detailed description of the complaint
- **Priority Level**: HIGH, MEDIUM (default), or LOW

## Email Format

The form sends emails in a structured format that the email processor can easily parse:

```
Subject: Complaint: [Company Name] - [Priority] Priority

Body:
Dear CarePilot - the customer's co-pilot Team,

I would like to raise a complaint regarding [Company Name].

Customer Information:
- Name: [Customer Name]
- Email: [Customer Email]
- Phone: [Phone Number]
- Priority: [Priority]

Problem Description:
[Problem Description]

Please process this complaint and ensure it reaches the appropriate team for resolution.

Thank you,
[Customer Name]
```

## Integration with Email Processor

The landing page sends emails to: `reachus.sherlox@gmail.com`

The email processor agent will:
1. Receive the email
2. Extract customer information (name, email, phone)
3. Analyze the complaint description
4. Determine priority level
5. Process and route to the appropriate team

## Customization

### Colors
Edit the CSS variables in `styles.css`:
```css
:root {
    --primary-color: #6366f1;
    --primary-dark: #4f46e5;
    --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* ... */
}
```

### Target Email
Change the target email in `script.js`:
```javascript
const TARGET_EMAIL = 'reachus.sherlox@gmail.com';
```

## Deployment

### Quick Deploy (5 minutes)

For the fastest deployment, see [QUICK_DEPLOY.md](./QUICK_DEPLOY.md)

### Full Deployment Guide

For detailed deployment instructions including:
- Multiple hosting options (Netlify, Vercel, GitHub Pages, AWS)
- CORS configuration
- Production setup
- Troubleshooting

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

### Pre-Deployment Checklist

Before deploying to production:
1. Update `dashboard.js`: Set `USE_LOCAL_PROXY = false`
2. Verify CRM server CORS configuration
3. Test all functionality locally
4. Review deployment guide for your chosen platform

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is part of the CarePilot - the customer's co-pilot system.

