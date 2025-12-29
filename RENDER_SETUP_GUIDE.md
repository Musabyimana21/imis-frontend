# RENDER + CPANEL DEPLOYMENT GUIDE

## 🎯 Setup: Backend on Render + Frontend on cPanel

### Step 1: Deploy Backend to Render

1. **Create PostgreSQL Database on Render:**
   - Go to https://dashboard.render.com
   - Click "New +" → "PostgreSQL"
   - Name: `imis-database`
   - Plan: Free
   - **COPY the Internal Database URL**

2. **Create Web Service:**
   - Click "New +" → "Web Service"
   - Connect GitHub repo: your IMIS repository
   - Name: `imis-backend`
   - Environment: `Python 3`
   - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
   - Start Command: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Set Environment Variables in Render:**
   ```
   DATABASE_URL = [Your PostgreSQL URL from step 1]
   SECRET_KEY = a8f5f167f44f4964e6c998dee827110c
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   FRONTEND_URL = https://e-shakiro.com
   ALLOWED_ORIGINS = https://e-shakiro.com,http://e-shakiro.com
   MTN_MOMO_ENABLED = true
   MTN_MOMO_ENVIRONMENT = production
   MTN_MOMO_BASE_URL = https://proxy.momoapi.mtn.co.rw
   MTN_MOMO_SUBSCRIPTION_KEY = 92e0ee9794d34ac8bb166d2cd3b99a69
   MTN_MOMO_API_USER = 24a14d7b-57b2-46a6-ba5c-4c17f628eb9e
   MTN_MOMO_API_KEY = 2ac93c3f60304fdaa6f9ad2f591f0834
   MTN_MOMO_TARGET_ENVIRONMENT = mtnrwanda
   MTN_MOMO_CALLBACK_URL = https://e-shakiro.com/api/anonymous/payment/callback
   MTN_MOMO_CALLBACK_HOST = e-shakiro.com
   ```

4. **Deploy:**
   - Push code to GitHub
   - Render will auto-deploy
   - **Note your Render URL** (e.g., `https://imis-backend-xyz.onrender.com`)

### Step 2: Update Frontend for cPanel

1. **Update frontend environment:**
   - Edit `frontend/.env.production`
   - Set `PUBLIC_API_URL` to your Render backend URL

2. **Build frontend for production:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. **Upload to cPanel:**
   - Upload contents of `frontend/build/` or `frontend/dist/` to your cPanel public_html
   - Update any hardcoded API URLs to point to Render

### Step 3: Test the Setup

1. **Backend Health Check:**
   - Visit: `https://your-render-url.onrender.com/health`
   - Should return: `{"status": "healthy", "database": "connected"}`

2. **Frontend Test:**
   - Visit your cPanel domain
   - Test login/registration
   - Verify API calls work

## 🔧 Quick Fix Commands

**Update Frontend API URL:**
```bash
# In frontend folder
echo "PUBLIC_API_URL=https://your-render-url.onrender.com" > .env.production
npm run build
```

**Test Backend:**
```bash
curl https://your-render-url.onrender.com/health
```

## 📋 Checklist

- [ ] PostgreSQL database created on Render
- [ ] Web service deployed with correct environment variables
- [ ] Backend health check passes
- [ ] Frontend built with correct API URL
- [ ] Frontend uploaded to cPanel
- [ ] End-to-end testing completed

## 🚨 Important Notes

- **Free Render**: Backend sleeps after 15 minutes of inactivity
- **CORS**: Already configured for e-shakiro.com
- **Database**: Use PostgreSQL, not SQLite on Render
- **SSL**: Render provides HTTPS automatically