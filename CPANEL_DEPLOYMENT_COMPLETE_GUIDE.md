# IMIS cPanel Deployment Guide for e-shakiro.com

## Prerequisites ✅
- [x] Backend running locally (http://localhost:8000)
- [x] Database configured (MySQL on cPanel)
- [x] Domain: e-shakiro.com
- [x] cPanel access

## Step 1: Prepare Files for Upload

### Run Deployment Script
```bash
DEPLOY_TO_CPANEL.bat
```

This creates a `cpanel_deploy` folder with:
- Backend files (ready for cPanel Python app)
- Frontend build files
- Configuration files

## Step 2: cPanel Backend Setup

### 2.1 Upload Backend Files
1. **cPanel File Manager** → Navigate to `public_html`
2. **Create folder**: `api`
3. **Upload** all files from `cpanel_deploy/backend/` to `public_html/api/`

### 2.2 Create Python App
1. **cPanel** → **Python App**
2. **Create Application**:
   - **Python Version**: 3.8+ (latest available)
   - **Application Root**: `/public_html/api`
   - **Application URL**: `e-shakiro.com/api`
   - **Application Startup File**: `passenger_wsgi.py`

### 2.3 Install Dependencies
1. **Open Python App Terminal**
2. **Run**:
   ```bash
   pip install -r requirements.txt
   ```

### 2.4 Configure Environment
1. **Verify** `.env` file is in `/public_html/api/`
2. **Check** database connection settings
3. **Restart** Python application

## Step 3: cPanel Frontend Setup

### 3.1 Build Frontend
```bash
cd frontend
npm run build
```

### 3.2 Upload Frontend Files
1. **Upload** contents of `frontend/build/` to `public_html/`
2. **Upload** `.htaccess` to `public_html/`

## Step 4: Database Setup

### 4.1 Verify Database User
- **Database**: `eshakiro_imis_production`
- **User**: `eshakiro_imis_user`
- **Password**: `Bachjudoly@11996`

### 4.2 Test Connection
Visit: `https://e-shakiro.com/api/health`
Expected: `{"status":"healthy","database":"connected","version":"3.0.0"}`

## Step 5: DNS & SSL

### 5.1 SSL Certificate
1. **cPanel** → **SSL/TLS**
2. **Let's Encrypt** → Enable for `e-shakiro.com`

### 5.2 Force HTTPS
Add to `.htaccess`:
```apache
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

## Step 6: Testing

### 6.1 Backend Tests
- ✅ `https://e-shakiro.com/api/health`
- ✅ `https://e-shakiro.com/api/docs`
- ✅ `https://e-shakiro.com/api/v1/auth/register`

### 6.2 Frontend Tests
- ✅ `https://e-shakiro.com` (homepage loads)
- ✅ Navigation works
- ✅ API calls successful

## Step 7: Production Checklist

### Security
- [ ] SSL certificate active
- [ ] Database user has minimal permissions
- [ ] Environment variables secure
- [ ] CORS configured correctly

### Performance
- [ ] Static files cached
- [ ] Database indexed
- [ ] Images optimized

### Monitoring
- [ ] Error logging enabled
- [ ] Health check endpoint working
- [ ] Payment system tested

## Troubleshooting

### Common Issues

**Backend not starting:**
- Check Python version compatibility
- Verify all dependencies installed
- Check `.env` file permissions

**Database connection failed:**
- Verify database credentials
- Check Remote Database Access IPs
- Test connection from cPanel

**Frontend 404 errors:**
- Check `.htaccess` file uploaded
- Verify build files in correct location
- Check file permissions

**CORS errors:**
- Update `ALLOWED_ORIGINS` in backend
- Check `.htaccess` CORS headers
- Verify API URL in frontend

## Support Commands

### Check Python App Status
```bash
# In cPanel Python App terminal
ps aux | grep python
```

### View Logs
```bash
tail -f logs/error.log
tail -f logs/access.log
```

### Restart Services
- **Python App**: Restart in cPanel
- **Apache**: Contact hosting provider

## Final URLs
- **Frontend**: https://e-shakiro.com
- **Backend API**: https://e-shakiro.com/api
- **API Docs**: https://e-shakiro.com/api/docs
- **Health Check**: https://e-shakiro.com/api/health