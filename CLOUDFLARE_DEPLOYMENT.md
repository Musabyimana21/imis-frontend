# IMIS Frontend - Cloudflare Pages Deployment Guide

## ✅ Pre-Deployment Checklist

- [x] Backend deployed: https://imis-backend-wk7z.onrender.com
- [x] Frontend configured with correct API URL
- [x] SvelteKit with static adapter
- [x] All dependencies in package.json

## 🚀 Deployment Steps

### Step 1: Create GitHub Repository for Frontend

1. Go to https://github.com/Musabyimana21
2. Click **"New"** repository
3. Name: `imis-frontend`
4. Description: `IMIS Frontend - Lost & Found Platform for Rwanda`
5. **Public** or Private (your choice)
6. **DO NOT** initialize with README
7. Click **"Create repository"**

### Step 2: Push Frontend Code to GitHub

Run these commands in `T:\IMIS\frontend`:

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial IMIS frontend deployment"

# Add remote (replace with your actual repo URL)
git remote add origin https://github.com/Musabyimana21/imis-frontend.git

# Push
git push -u origin main
```

### Step 3: Deploy to Cloudflare Pages

1. Go to https://dash.cloudflare.com
2. Click **"Workers & Pages"** in left sidebar
3. Click **"Create application"**
4. Click **"Pages"** tab
5. Click **"Connect to Git"**
6. Select **GitHub** and authorize Cloudflare
7. Select **"imis-frontend"** repository
8. Configure build settings:
   - **Project name**: `imis-frontend`
   - **Production branch**: `main`
   - **Framework preset**: `SvelteKit`
   - **Build command**: `npm run build`
   - **Build output directory**: `build`

9. **Environment variables** (click "Add variable"):
   - Key: `PUBLIC_API_URL`
   - Value: `https://imis-backend-wk7z.onrender.com`

10. Click **"Save and Deploy"**

### Step 4: Wait for Deployment

- Build time: 2-3 minutes
- You'll get a URL like: `https://imis-frontend.pages.dev`

### Step 5: Update Backend CORS

After deployment, update backend to allow your Cloudflare URL:

1. Go to backend `app/main.py`
2. Add your Cloudflare URL to `allow_origins`:
   ```python
   allow_origins=[
       "http://localhost:5173",
       "https://imis-frontend.pages.dev",  # Add this
       "https://*.pages.dev",
   ]
   ```
3. Commit and push to trigger backend redeploy

## 🧪 Verification

After deployment:

1. **Visit your site**: https://imis-frontend.pages.dev
2. **Test features**:
   - Homepage loads
   - Can view lost/found items
   - Can register/login
   - Can report items
   - Map works

## 📝 Environment Variables

Cloudflare Pages will use:
- `PUBLIC_API_URL=https://imis-backend-wk7z.onrender.com`

## 🔧 Build Configuration

```json
{
  "build": {
    "command": "npm run build",
    "output": "build"
  }
}
```

## 🎯 Success Criteria

✅ Build completes without errors
✅ Site is accessible
✅ API calls work
✅ All pages load correctly
✅ No CORS errors

## 📞 Support

Issues? Contact: gaudencemusabyimana21@gmail.com
