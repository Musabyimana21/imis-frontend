@echo off
setlocal enabledelayedexpansion

echo ========================================
echo IMIS Safe Deployment Solution
echo ========================================
echo.

cd /d "%~dp0"

:: Check if Node.js is available (with timeout)
echo Checking Node.js availability...
timeout /t 2 >nul
where node >nul 2>&1
set NODE_AVAILABLE=%errorlevel%

:: Check if build directory exists
if exist "frontend\build" (
    set BUILD_EXISTS=1
    echo ✅ Frontend build directory found
) else (
    set BUILD_EXISTS=0
    echo ❌ Frontend build directory not found
)

echo.
echo System Status:
if %NODE_AVAILABLE% equ 0 (
    echo ✅ Node.js: Available
) else (
    echo ❌ Node.js: Not found - Install from https://nodejs.org/
)
echo.

:: Create deployment directory
echo Creating deployment package...
if exist "cpanel_deploy" rmdir /s /q "cpanel_deploy"
mkdir cpanel_deploy
mkdir cpanel_deploy\backend
mkdir cpanel_deploy\frontend

:: Always copy backend files
echo.
echo 📁 Copying backend files...
xcopy "backend\app" "cpanel_deploy\backend\app" /E /I /Y >nul
xcopy "backend\*.py" "cpanel_deploy\backend\" /Y >nul
copy "backend\.env.cpanel" "cpanel_deploy\backend\.env" >nul
copy "backend\requirements.txt" "cpanel_deploy\backend\" >nul
copy "backend\passenger_wsgi.py" "cpanel_deploy\backend\" >nul
echo ✅ Backend files copied successfully

:: Handle frontend - NO HANGING
echo.
echo 🌐 Processing frontend...

if %BUILD_EXISTS% equ 1 (
    echo ✅ Using existing build files
    xcopy "frontend\build" "cpanel_deploy\frontend\" /E /I /Y >nul
    copy "frontend\.htaccess" "cpanel_deploy\frontend\" >nul 2>nul
    echo ✅ Built frontend files copied
    set FRONTEND_STATUS=READY
) else (
    echo 📄 Copying source files (build required)
    xcopy "frontend\src" "cpanel_deploy\frontend\src" /E /I /Y >nul
    xcopy "frontend\static" "cpanel_deploy\frontend\static" /E /I /Y >nul
    copy "frontend\package.json" "cpanel_deploy\frontend\" >nul
    copy "frontend\svelte.config.js" "cpanel_deploy\frontend\" >nul 2>nul
    copy "frontend\vite.config.js" "cpanel_deploy\frontend\" >nul 2>nul
    copy "frontend\tailwind.config.js" "cpanel_deploy\frontend\" >nul 2>nul
    copy "frontend\postcss.config.js" "cpanel_deploy\frontend\" >nul 2>nul
    copy "frontend\.htaccess" "cpanel_deploy\frontend\" >nul 2>nul
    copy "frontend\.env.production" "cpanel_deploy\frontend\.env" >nul 2>nul
    echo ⚠️  Source files copied - manual build required
    set FRONTEND_STATUS=BUILD_NEEDED
)

:: Create simple deployment guide
echo.
echo 📋 Creating deployment guide...

(
echo # IMIS Quick Deployment Guide
echo.
echo ## Status
if "%FRONTEND_STATUS%"=="READY" (
    echo ✅ **Ready for deployment** - Built files included
) else (
    echo ⚠️  **Build required** - Source files only
)
echo.
echo ## Upload Instructions
echo.
echo ### Backend
echo 1. Upload `backend/` folder contents to `public_html/api/`
echo 2. Create Python App in cPanel
echo 3. Install requirements: `pip install -r requirements.txt`
echo.
echo ### Frontend
if "%FRONTEND_STATUS%"=="READY" (
    echo 1. Upload `frontend/` folder contents to `public_html/`
) else (
    echo 1. **First install Node.js**: https://nodejs.org/
    echo 2. **Build frontend**: `cd frontend && npm install && npm run build`
    echo 3. **Then upload** `build/` contents to `public_html/`
)
echo.
echo ## Database Setup
echo ```
echo Database: eshakiro_imis_production
echo User: eshakiro_imis_user
echo Password: Bachjudoly@11996
echo ```
echo.
echo ## Test URLs
echo - Backend: https://e-shakiro.com/api/health
echo - Frontend: https://e-shakiro.com
echo - API Docs: https://e-shakiro.com/api/docs
) > cpanel_deploy\QUICK_DEPLOY_GUIDE.md

:: Create .htaccess
(
echo RewriteEngine On
echo RewriteCond %%{HTTPS} off
echo RewriteRule ^^(.*)$ https://%%{HTTP_HOST}%%{REQUEST_URI} [L,R=301]
echo RewriteRule ^^api/(.*)$ /api/$1 [L]
echo RewriteCond %%{REQUEST_FILENAME} !-f
echo RewriteCond %%{REQUEST_FILENAME} !-d
echo RewriteRule . /index.html [L]
) > cpanel_deploy\frontend\.htaccess

echo ✅ Deployment package created

:: Summary
echo.
echo ========================================
echo 🎉 DEPLOYMENT PACKAGE READY
echo ========================================
echo.
echo 📦 Location: cpanel_deploy\
echo 📋 Guide: QUICK_DEPLOY_GUIDE.md
echo.

if "%FRONTEND_STATUS%"=="READY" (
    echo ✅ Status: Ready for immediate upload
) else (
    echo ⚠️  Status: Node.js installation required
    echo 💡 See: NODEJS_INSTALLATION_GUIDE.md
)

echo.
echo 🚀 Next: Compress cpanel_deploy folder and upload to cPanel
echo.
pause