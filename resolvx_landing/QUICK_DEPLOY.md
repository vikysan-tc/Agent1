# Quick Deployment Guide

## Fastest Way to Deploy (Netlify - 5 minutes)

### Step 1: Prepare Files
```bash
cd resolvx_landing
# Update dashboard.js for production
# Change: const USE_LOCAL_PROXY = true; → const USE_LOCAL_PROXY = false;
```

### Step 2: Deploy to Netlify

**Option A: Drag & Drop (Easiest)**
1. Go to [app.netlify.com](https://app.netlify.com)
2. Sign up/Login
3. Drag the `resolvx_landing` folder to the deploy area
4. Done! Your site is live

**Option B: Git Integration**
1. Push code to GitHub
2. Connect repository to Netlify
3. Auto-deploy on every push

### Step 3: Configure Custom Domain (Optional)
- Netlify Dashboard → Site Settings → Domain Management
- Add your custom domain

---

## Alternative: Vercel (Also 5 minutes)

```bash
cd resolvx_landing
npm install -g vercel
vercel --prod
```

Follow the prompts. Done!

---

## Important: CORS Configuration

**Before deploying, ensure one of these:**

1. **CRM Server has CORS enabled** (Best)
   - Server should allow requests from your domain
   - Headers: `Access-Control-Allow-Origin: https://your-domain.com`

2. **Use Netlify/Vercel Serverless Functions** (If CORS not available)
   - See `DEPLOYMENT_GUIDE.md` for serverless function examples

3. **Deploy Separate Proxy Server** (Last resort)
   - Deploy `proxy_server.py` to Railway/Render
   - Update `dashboard.js` to use proxy URL

---

## Post-Deployment Checklist

- [ ] Test landing page form
- [ ] Test dashboard data loading
- [ ] Check browser console for errors
- [ ] Test on mobile device
- [ ] Verify HTTPS is enabled

---

## Troubleshooting

**Dashboard not loading?**
- Check browser console (F12)
- Verify CRM server is accessible
- Check CORS headers in Network tab

**CORS errors?**
- See CORS configuration section above
- Or use serverless function proxy (see full guide)

---

For detailed instructions, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

