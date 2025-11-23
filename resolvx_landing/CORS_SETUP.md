# CORS Setup Guide

This guide explains how to handle CORS (Cross-Origin Resource Sharing) issues when running the landing page locally.

## Problem

When accessing the CRM API from `localhost:8000`, browsers block the request due to CORS policy because the server doesn't send the required CORS headers.

## Solution Options

### Option 1: Use Local Proxy Server (Recommended) ⭐

This is the easiest and most reliable solution for local development.

#### Step 1: Start the Proxy Server

Open a new terminal and run:

```bash
cd resolvx_landing
python proxy_server.py
```

The proxy server will run on `http://localhost:8001` and automatically add CORS headers to all requests.

#### Step 2: Start the Landing Page Server

In another terminal:

```bash
cd resolvx_landing
python -m http.server 8000
```

#### Step 3: Access the Landing Page

Open `http://localhost:8000` in your browser. The dashboard and metrics bar will now work without CORS errors.

**Note:** The proxy server must be running for the dashboard to work. Keep both terminals open.

---

### Option 2: Browser Extension (Quick Fix for Testing)

For quick testing, you can use a browser extension to disable CORS:

#### Chrome:
1. Install "CORS Unblock" or "Allow CORS: Access-Control-Allow-Origin" extension
2. Enable the extension
3. Refresh the page

#### Firefox:
1. Install "CORS Everywhere" extension
2. Enable the extension
3. Refresh the page

**⚠️ Warning:** Only use browser extensions for local development. Never disable CORS in production browsers.

---

### Option 3: Use a Public CORS Proxy (Not Recommended)

You can use a public CORS proxy service, but this is **not recommended** for production:

1. Update `dashboard.js` and `script.js` to use a CORS proxy URL
2. Example: `https://cors-anywhere.herokuapp.com/https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver/api/tickets`

**⚠️ Warning:** Public CORS proxies are unreliable and may have rate limits or security concerns.

---

### Option 4: Configure Server CORS (Best for Production)

If you have access to the CRM server, configure it to send proper CORS headers:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Accept
```

---

## Quick Start (Recommended Method)

1. **Terminal 1** - Start proxy server:
   ```bash
   cd resolvx_landing
   python proxy_server.py
   ```

2. **Terminal 2** - Start landing page:
   ```bash
   cd resolvx_landing
   python -m http.server 8000
   ```

3. Open browser: `http://localhost:8000`

That's it! The dashboard should now work without CORS errors.

---

## Troubleshooting

### Proxy server won't start
- Make sure port 8001 is not in use
- Check if Python is installed: `python --version`
- Try a different port: `python proxy_server.py 8002`

### Still getting CORS errors
- Make sure the proxy server is running
- Check browser console for errors
- Verify `USE_LOCAL_PROXY = true` in `dashboard.js` and `script.js`

### Dashboard shows "-" for metrics
- Check if proxy server is running
- Check browser console for errors
- Verify the CRM server URL is correct

---

## Production Deployment

For production, you should:
1. Configure the CRM server to send proper CORS headers
2. Remove the proxy server dependency
3. Set `USE_LOCAL_PROXY = false` in the JavaScript files

