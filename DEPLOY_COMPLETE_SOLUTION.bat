@echo off
setlocal enabledelayedexpansion

echo ========================================
echo IMIS Complete Deployment Solution
echo ========================================
echo.

cd /d "%~dp0"

:: Check current status
echo Checking system requirements...
echo.

:: Check if Node.js is available
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

:: Check if .svelte-kit exists (development setup)
if exist "frontend\.svelte-kit" (
    set DEV_SETUP=1
    echo ✅ Development environment detected
) else (
    set DEV_SETUP=0
    echo ❌ Development environment not found
)

echo.
echo System Status:
if %NODE_AVAILABLE% equ 0 (
    echo ✅ Node.js: Available
) else (
    echo ❌ Node.js: Not found
)
echo Build files: !BUILD_EXISTS!
echo Dev setup: !DEV_SETUP!
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

:: Handle frontend based on available options
echo.
echo 🌐 Processing frontend...

if %BUILD_EXISTS% equ 1 (
    echo ✅ Using existing build files
    xcopy "frontend\build" "cpanel_deploy\frontend\" /E /I /Y >nul
    copy "frontend\.htaccess" "cpanel_deploy\frontend\" >nul 2>nul
    echo ✅ Built frontend files copied
    goto create_instructions
)

if %NODE_AVAILABLE% equ 0 (
    echo 🔨 Building frontend with Node.js...
    cd frontend
    
    :: Install dependencies if needed
    if not exist "node_modules" (
        echo Installing dependencies...
        call npm install
        if !errorlevel! neq 0 (
            echo ❌ npm install failed
            cd ..
            goto copy_source
        )
    )
    
    :: Build the project
    echo Building production files...
    call npm run build
    if !errorlevel! neq 0 (
        echo ❌ Build failed, copying source files instead
        cd ..
        goto copy_source
    )
    
    cd ..
    echo ✅ Frontend built successfully
    xcopy "frontend\build" "cpanel_deploy\frontend\" /E /I /Y >nul
    copy "frontend\.htaccess" "cpanel_deploy\frontend\" >nul 2>nul
    goto create_instructions
)

:copy_source
echo 📄 Copying source files (Node.js not available)
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

:create_instructions

:: Create comprehensive deployment guide
echo.
echo 📋 Creating deployment instructions...

(
echo # IMIS cPanel Deployment Guide
echo.
echo ## 🚀 Quick Start
echo.
echo ### Backend Deployment
echo 1. **Upload backend files** to `public_html/api/`
echo 2. **Create Python App** in cPanel:
echo    - Application Root: `/public_html/api`
echo    - Startup File: `passenger_wsgi.py`
echo    - Python Version: 3.8+
echo 3. **Install dependencies**: `pip install -r requirements.txt`
echo.
echo ### Frontend Deployment
if %BUILD_EXISTS% equ 1 (
    echo ✅ **Built files ready** - Upload `frontend/` contents to `public_html/`
) else if %NODE_AVAILABLE% equ 0 (
    echo ✅ **Built files created** - Upload `frontend/` contents to `public_html/`
) else (
    echo ⚠️  **Source files only** - Build required before upload
    echo.
    echo **To build frontend:**
    echo 1. Install Node.js from https://nodejs.org/
    echo 2. Run: `cd frontend && npm install && npm run build`
    echo 3. Upload `build/` contents to `public_html/`
)
echo.
echo ## 🔧 Detailed Setup
echo.
echo ### Database Configuration
echo ```
echo Database: eshakiro_imis_production
echo User: eshakiro_imis_user  
echo Password: Bachjudoly@11996
echo Host: localhost
echo ```
echo.
echo ### Environment Variables
echo Ensure `.env` file in backend contains:
echo ```
echo DATABASE_URL=mysql://eshakiro_imis_user:Bachjudoly@11996@localhost/eshakiro_imis_production
echo SECRET_KEY=your-secret-key
echo ALLOWED_ORIGINS=https://e-shakiro.com,https://www.e-shakiro.com
echo ```
echo.
echo ### SSL Setup
echo 1. Enable SSL in cPanel
echo 2. Force HTTPS redirect
echo 3. Update API URLs to use HTTPS
echo.
echo ## 🧪 Testing
echo.
echo ### Backend Health Check
echo Visit: `https://e-shakiro.com/api/health`
echo Expected: `{"status":"healthy","database":"connected"}`
echo.
echo ### API Documentation  
echo Visit: `https://e-shakiro.com/api/docs`
echo.
echo ### Frontend Test
echo Visit: `https://e-shakiro.com`
echo.
echo ## 🔍 Troubleshooting
echo.
echo ### Common Issues
echo - **Python app won't start**: Check Python version and dependencies
echo - **Database connection failed**: Verify credentials and Remote MySQL
echo - **CORS errors**: Update ALLOWED_ORIGINS in .env
echo - **404 errors**: Check .htaccess file uploaded
echo.
echo ### Support Commands
echo ```bash
echo # Check Python app status
echo ps aux ^| grep python
echo.
echo # View logs
echo tail -f logs/error.log
echo ```
echo.
echo ## 📞 Support
echo If you need help:
echo 1. Check cPanel error logs
echo 2. Verify all files uploaded correctly
echo 3. Test each component individually
) > cpanel_deploy\DEPLOYMENT_GUIDE.md

:: Create a simple test page
(
echo ^<!DOCTYPE html^>
echo ^<html lang="en"^>
echo ^<head^>
echo     ^<meta charset="UTF-8"^>
echo     ^<meta name="viewport" content="width=device-width, initial-scale=1.0"^>
echo     ^<title^>IMIS - Deployment Test^</title^>
echo     ^<style^>
echo         body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
echo         .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
echo         .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
echo         .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
echo     ^</style^>
echo ^</head^>
echo ^<body^>
echo     ^<h1^>🏥 IMIS - Ishakiro Information Management System^</h1^>
echo     ^<div class="status success"^>
echo         ^<strong^>✅ Frontend Deployed Successfully^</strong^>
echo         ^<p^>If you can see this page, the frontend deployment is working correctly.^</p^>
echo     ^</div^>
echo     
echo     ^<div class="status info"^>
echo         ^<strong^>🔗 Test Links^</strong^>
echo         ^<ul^>
echo             ^<li^>^<a href="/api/health" target="_blank"^>Backend Health Check^</a^>^</li^>
echo             ^<li^>^<a href="/api/docs" target="_blank"^>API Documentation^</a^>^</li^>
echo             ^<li^>^<a href="/" target="_blank"^>Main Application^</a^>^</li^>
echo         ^</ul^>
echo     ^</div^>
echo     
echo     ^<h2^>Next Steps^</h2^>
echo     ^<ol^>
echo         ^<li^>Test the backend health check link above^</li^>
echo         ^<li^>Verify API documentation is accessible^</li^>
echo         ^<li^>Test the main application functionality^</li^>
echo     ^</ol^>
echo ^</body^>
echo ^</html^>
) > cpanel_deploy\frontend\deployment-test.html

:: Create .htaccess for proper routing
(
echo RewriteEngine On
echo.
echo # Force HTTPS
echo RewriteCond %%{HTTPS} off
echo RewriteRule ^^(.*)$ https://%%{HTTP_HOST}%%{REQUEST_URI} [L,R=301]
echo.
echo # API routing
echo RewriteRule ^^api/(.*)$ /api/$1 [L]
echo.
echo # SPA routing - send all non-file requests to index.html
echo RewriteCond %%{REQUEST_FILENAME} !-f
echo RewriteCond %%{REQUEST_FILENAME} !-d
echo RewriteRule . /index.html [L]
echo.
echo # CORS headers
echo Header always set Access-Control-Allow-Origin "*"
echo Header always set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
echo Header always set Access-Control-Allow-Headers "Content-Type, Authorization"
) > cpanel_deploy\frontend\.htaccess

echo ✅ Deployment instructions created

:: Summary
echo.
echo ========================================
echo 🎉 DEPLOYMENT PACKAGE READY
echo ========================================
echo.
echo 📦 Package location: cpanel_deploy\
echo 📋 Instructions: DEPLOYMENT_GUIDE.md
echo 🧪 Test page: deployment-test.html
echo.

if %BUILD_EXISTS% equ 1 (
    echo ✅ Status: Ready for immediate deployment
    echo 📁 Frontend: Built files included
) else if %NODE_AVAILABLE% equ 0 (
    echo ✅ Status: Built and ready for deployment  
    echo 📁 Frontend: Freshly built files included
) else (
    echo ⚠️  Status: Manual build required
    echo 📁 Frontend: Source files only
    echo.
    echo 💡 To complete setup:
    echo 1. Install Node.js: https://nodejs.org/
    echo 2. Run: NODEJS_INSTALLATION_GUIDE.md
    echo 3. Re-run this script
)

echo.
echo 🚀 Next Steps:
echo 1. Compress 'cpanel_deploy' folder to ZIP
echo 2. Upload to cPanel File Manager  
echo 3. Follow DEPLOYMENT_GUIDE.md
echo 4. Test using deployment-test.html
echo.
pause