@echo off
echo ========================================
echo IMIS cPanel Deployment Package Creator
echo ========================================
echo.

cd /d "%~dp0"

echo Creating deployment package...
echo.

:: Create deployment directory
if exist "cpanel_deploy" rmdir /s /q "cpanel_deploy"
mkdir cpanel_deploy
mkdir cpanel_deploy\backend
mkdir cpanel_deploy\frontend

:: Copy backend files
echo Copying backend files...
xcopy "backend\app" "cpanel_deploy\backend\app" /E /I /Y
xcopy "backend\*.py" "cpanel_deploy\backend\" /Y
copy "backend\.env.cpanel" "cpanel_deploy\backend\.env"
copy "backend\requirements.txt" "cpanel_deploy\backend\"

:: Check if Node.js is available
echo Checking for Node.js...
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Node.js not found. Copying source files instead of building.
    echo You'll need to build the frontend manually or use the pre-built version.
    echo.
    echo Copying frontend source files...
    xcopy "frontend\src" "cpanel_deploy\frontend\src" /E /I /Y
    xcopy "frontend\static" "cpanel_deploy\frontend\static" /E /I /Y
    copy "frontend\package.json" "cpanel_deploy\frontend\"
    copy "frontend\svelte.config.js" "cpanel_deploy\frontend\"
    copy "frontend\vite.config.js" "cpanel_deploy\frontend\"
    copy "frontend\tailwind.config.js" "cpanel_deploy\frontend\"
    copy "frontend\postcss.config.js" "cpanel_deploy\frontend\"
    copy "frontend\.htaccess" "cpanel_deploy\frontend\"
    copy "frontend\.env.production" "cpanel_deploy\frontend\.env"
    goto skip_build
)

:: Try to build frontend
echo Building frontend...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: npm install failed. Copying source files instead.
    cd ..
    goto copy_source
)

call npm run build
if %errorlevel% neq 0 (
    echo ERROR: npm build failed. Copying source files instead.
    cd ..
    goto copy_source
)

cd ..
echo Copying built frontend files...
xcopy "frontend\build" "cpanel_deploy\frontend\" /E /I /Y
copy "frontend\.htaccess" "cpanel_deploy\frontend\"
goto skip_build

:copy_source
echo Copying frontend source files...
xcopy "frontend\src" "cpanel_deploy\frontend\src" /E /I /Y
xcopy "frontend\static" "cpanel_deploy\frontend\static" /E /I /Y
copy "frontend\package.json" "cpanel_deploy\frontend\"
copy "frontend\svelte.config.js" "cpanel_deploy\frontend\"
copy "frontend\vite.config.js" "cpanel_deploy\frontend\"
copy "frontend\tailwind.config.js" "cpanel_deploy\frontend\"
copy "frontend\postcss.config.js" "cpanel_deploy\frontend\"
copy "frontend\.htaccess" "cpanel_deploy\frontend\"
copy "frontend\.env.production" "cpanel_deploy\frontend\.env"

:skip_build

:: Create comprehensive deployment instructions
echo Creating deployment instructions...
(
echo # IMIS cPanel Deployment Instructions
echo.
echo ## Prerequisites
echo - cPanel hosting account with Python support
echo - MySQL database access
echo - Domain: e-shakiro.com
echo.
echo ## Backend Deployment
echo.
echo ### 1. Upload Backend Files
echo 1. Upload all files from `backend/` folder to `public_html/api/`
echo 2. Ensure `.env` file is uploaded with correct database credentials
echo.
echo ### 2. Create Python Application
echo 1. Go to cPanel ^> Python App
echo 2. Create new application:
echo    - Python Version: 3.8+ ^(latest available^)
echo    - Application Root: `/public_html/api`
echo    - Application URL: `e-shakiro.com/api`
echo    - Application Startup File: `passenger_wsgi.py`
echo.
echo ### 3. Install Dependencies
echo 1. Open Python App terminal
echo 2. Run: `pip install -r requirements.txt`
echo.
echo ## Frontend Deployment
echo.
echo ### Option 1: If you have built files ^(build folder exists^)
echo 1. Upload contents of `frontend/` to `public_html/`
echo 2. Upload `.htaccess` to `public_html/`
echo.
echo ### Option 2: If you have source files ^(Node.js not available^)
echo 1. Install Node.js on your local machine
echo 2. Run `npm install` in frontend folder
echo 3. Run `npm run build`
echo 4. Upload generated `build/` contents to `public_html/`
echo 5. Upload `.htaccess` to `public_html/`
echo.
echo ### Option 3: Use Cloudflare Pages ^(Recommended^)
echo 1. Connect your repository to Cloudflare Pages
echo 2. Set build command: `npm run build`
echo 3. Set output directory: `build`
echo 4. Deploy automatically
echo.
echo ## Database Configuration
echo.
echo ### Database Details
echo - Database: `eshakiro_imis_production`
echo - User: `eshakiro_imis_user`
echo - Password: `Bachjudoly@11996`
echo - Host: `localhost`
echo.
echo ### Test Connection
echo Visit: `https://e-shakiro.com/api/health`
echo Expected: `{"status":"healthy","database":"connected","version":"3.0.0"}`
echo.
echo ## SSL and Security
echo.
echo 1. Enable SSL certificate in cPanel
echo 2. Force HTTPS redirect
echo 3. Update CORS settings if needed
echo.
echo ## Testing
echo.
echo ### Backend Tests
echo - https://e-shakiro.com/api/health
echo - https://e-shakiro.com/api/docs
echo.
echo ### Frontend Tests
echo - https://e-shakiro.com ^(homepage^)
echo - Navigation and API calls
echo.
echo ## Troubleshooting
echo.
echo ### Common Issues
echo - **Python app not starting**: Check Python version and dependencies
echo - **Database connection failed**: Verify credentials and host
echo - **CORS errors**: Update allowed origins in backend
echo - **404 errors**: Check .htaccess file and routing
echo.
echo ### Support
echo - Check Python app logs in cPanel
echo - Verify file permissions
echo - Test API endpoints individually
) > cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md

:: Create a simple HTML file for testing
(
echo ^<!DOCTYPE html^>
echo ^<html^>
echo ^<head^>
echo     ^<title^>IMIS - Test Page^</title^>
echo ^</head^>
echo ^<body^>
echo     ^<h1^>IMIS Deployment Test^</h1^>
echo     ^<p^>If you see this page, the frontend deployment is working.^</p^>
echo     ^<p^>^<a href="/api/health"^>Test Backend API^</a^>^</p^>
echo ^</body^>
echo ^</html^>
) > cpanel_deploy\frontend\test.html

echo.
echo ✅ Deployment package created in 'cpanel_deploy' folder
echo.
echo Next steps:
echo 1. Compress cpanel_deploy folder to ZIP
echo 2. Upload to cPanel File Manager
echo 3. Follow DEPLOYMENT_INSTRUCTIONS.md
echo.
echo Note: Frontend build failed due to missing Node.js
echo Consider installing Node.js for optimal deployment
echo.
pause