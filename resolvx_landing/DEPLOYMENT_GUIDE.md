# Deployment Guide - Landing Page & Dashboard

This guide covers deploying the CarePilot landing page and dashboard to production.

## Overview

The landing page consists of:
- **Landing Page** (`index.html`) - Customer complaint submission form
- **Dashboard** (`dashboard.html`) - Real-time ticket analytics and management
- **Static Assets** - CSS, JavaScript, and other resources

## Prerequisites

- CRM Server URL (already deployed): `https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver`
- Git repository (for Git-based deployments)
- Account on your chosen hosting platform

## Pre-Deployment Configuration

### Step 1: Update Dashboard Configuration for Production

Before deploying, update `dashboard.js` to use the production CRM API directly (without proxy):

```javascript
// In dashboard.js, change:
const USE_LOCAL_PROXY = false; // Set to false for production
const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';
```

### Step 2: Verify CORS Configuration

Ensure your CRM server allows requests from your production domain. The server should send these headers:

```
Access-Control-Allow-Origin: https://your-domain.com
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Accept
```

**Note:** If you don't have access to configure CORS on the CRM server, you may need to:
1. Deploy a production proxy server (see Option 4 below)
2. Or use a serverless function as a proxy (see Option 5 below)

---

## Deployment Options

### Option 1: Netlify (Recommended) ⭐

**Pros:** Easy setup, automatic HTTPS, custom domains, serverless functions support

#### Steps:

1. **Install Netlify CLI** (optional, for CLI deployment):
   ```bash
   npm install -g netlify-cli
   ```

2. **Create `netlify.toml`** in `resolvx_landing` folder:
   ```toml
   [build]
     publish = "."
     command = "echo 'No build step required'"

   [[redirects]]
     from = "/*"
     to = "/index.html"
     status = 200

   [build.environment]
     NODE_VERSION = "18"
   ```

3. **Deploy via Netlify Dashboard:**
   - Go to [netlify.com](https://netlify.com)
   - Drag and drop the `resolvx_landing` folder
   - Or connect your Git repository

4. **Deploy via CLI:**
   ```bash
   cd resolvx_landing
   netlify deploy --prod
   ```

5. **Configure Custom Domain** (optional):
   - In Netlify dashboard → Site settings → Domain management
   - Add your custom domain

#### Handle CORS with Netlify Functions (if needed):

Create `netlify/functions/cors-proxy.js`:
```javascript
exports.handler = async (event, context) => {
  const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';
  
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Accept',
      },
    };
  }
  
  try {
    const response = await fetch(`${CRM_SERVER_URL}${event.path.replace('/.netlify/functions/cors-proxy', '')}`, {
      method: event.httpMethod,
      headers: {
        'Accept': 'application/json',
      },
    });
    
    const data = await response.json();
    
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    };
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
};
```

Then update `dashboard.js`:
```javascript
const TICKETS_API_URL = '/.netlify/functions/cors-proxy/api/tickets';
```

---

### Option 2: Vercel

**Pros:** Fast deployment, automatic HTTPS, great for static sites

#### Steps:

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json`** in `resolvx_landing` folder:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "**",
         "use": "@vercel/static"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "/$1"
       }
     ]
   }
   ```

3. **Deploy:**
   ```bash
   cd resolvx_landing
   vercel --prod
   ```

4. **Handle CORS with Vercel Serverless Functions** (if needed):

   Create `api/cors-proxy.js`:
   ```javascript
   module.exports = async (req, res) => {
     const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';
     
     res.setHeader('Access-Control-Allow-Origin', '*');
     res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
     res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Accept');
     
     if (req.method === 'OPTIONS') {
       return res.status(200).end();
     }
     
     try {
       const response = await fetch(`${CRM_SERVER_URL}${req.url}`);
       const data = await response.json();
       res.json(data);
     } catch (error) {
       res.status(500).json({ error: error.message });
     }
   };
   ```

---

### Option 3: GitHub Pages

**Pros:** Free, easy for open-source projects

#### Steps:

1. **Push code to GitHub repository**

2. **Go to repository Settings → Pages**

3. **Select source branch** (usually `main` or `gh-pages`)

4. **Select folder** (root or `/docs`)

5. **Access your site** at `https://username.github.io/repository-name`

**Note:** GitHub Pages doesn't support serverless functions, so you'll need CORS configured on the CRM server or use a separate proxy service.

---

### Option 4: Deploy Proxy Server Separately

If CORS can't be configured on the CRM server, deploy the proxy server separately:

#### Using Python (Flask/FastAPI) on Railway/Render/Koyeb:

Create `proxy_app.py`:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver'

@app.route('/api/tickets', methods=['GET', 'POST', 'OPTIONS'])
def proxy_tickets():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        url = f"{CRM_SERVER_URL}/api/tickets"
        if request.method == 'GET':
            response = requests.get(url)
        else:
            response = requests.post(url, json=request.json)
        
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

Then update `dashboard.js`:
```javascript
const TICKETS_API_URL = 'https://your-proxy-server.com/api/tickets';
```

---

### Option 5: AWS S3 + CloudFront

**Pros:** Scalable, CDN support, custom domain

#### Steps:

1. **Create S3 Bucket:**
   ```bash
   aws s3 mb s3://carepilot-landing
   ```

2. **Upload files:**
   ```bash
   cd resolvx_landing
   aws s3 sync . s3://carepilot-landing --exclude "*.md" --exclude ".git/*"
   ```

3. **Configure S3 for static website hosting:**
   - Enable static website hosting
   - Set `index.html` as index document

4. **Create CloudFront distribution:**
   - Point to S3 bucket
   - Configure custom domain
   - Enable HTTPS

5. **Handle CORS with AWS Lambda@Edge** (if needed)

---

## Post-Deployment Checklist

- [ ] Update `dashboard.js` with production CRM URL
- [ ] Set `USE_LOCAL_PROXY = false` in `dashboard.js`
- [ ] Test landing page form submission
- [ ] Test dashboard data loading
- [ ] Verify CORS headers (check browser console)
- [ ] Test on mobile devices
- [ ] Configure custom domain (if applicable)
- [ ] Set up SSL/HTTPS certificate
- [ ] Test all links and navigation
- [ ] Verify email form opens Gmail correctly

---

## Environment-Specific Configuration

### Development
```javascript
// dashboard.js
const USE_LOCAL_PROXY = true;
const LOCAL_PROXY_URL = 'http://localhost:8001';
```

### Production
```javascript
// dashboard.js
const USE_LOCAL_PROXY = false;
const CRM_SERVER_URL = 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';
```

### Using Environment Variables (Advanced)

For platforms that support environment variables, you can make the configuration dynamic:

```javascript
// dashboard.js
const USE_LOCAL_PROXY = window.location.hostname === 'localhost';
const CRM_SERVER_URL = window.ENV?.CRM_SERVER_URL || 'https://desperate-bird-personal-viky-c10a64c7.koyeb.app/crmserver';
```

---

## Troubleshooting

### CORS Errors in Production

**Problem:** Browser blocks API requests due to CORS policy.

**Solutions:**
1. Configure CORS on CRM server (best solution)
2. Deploy a proxy server (see Option 4)
3. Use serverless functions (see Options 1 & 2)

### Dashboard Not Loading Data

**Check:**
- Browser console for errors
- Network tab for failed requests
- CRM server is accessible
- CORS headers are present

### Form Not Opening Gmail

**Check:**
- Browser allows `mailto:` links
- Email format is correct
- No popup blockers interfering

---

## Quick Deploy Commands

### Netlify
```bash
cd resolvx_landing
netlify deploy --prod
```

### Vercel
```bash
cd resolvx_landing
vercel --prod
```

### GitHub Pages
```bash
git push origin main
# Then configure in GitHub Settings → Pages
```

---

## Recommended Setup

For best results, we recommend:

1. **Landing Page & Dashboard:** Deploy to **Netlify** or **Vercel**
   - Easy setup
   - Automatic HTTPS
   - Custom domains
   - Serverless functions for CORS proxy (if needed)

2. **CORS Proxy (if needed):** Deploy to **Railway** or **Render**
   - Simple Flask/FastAPI app
   - Low cost
   - Easy to maintain

---

## Support

For issues or questions:
- Check browser console for errors
- Verify CRM server is running
- Test API endpoints directly
- Review CORS configuration

---

## Next Steps

After deployment:
1. Share the production URL with your team
2. Monitor error logs
3. Set up analytics (optional)
4. Configure custom domain
5. Set up monitoring/alerting

