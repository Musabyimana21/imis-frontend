@echo off
echo ========================================
echo    IMIS - Complete cPanel Deployment
echo    Domain: e-shakiro.com
echo ========================================

echo.
echo Step 1: Building Frontend for Production...
cd frontend
call npm install
call npm run build
cd ..

echo.
echo Step 2: Creating deployment package...
mkdir cpanel_deployment 2>nul
mkdir cpanel_deployment\frontend 2>nul
mkdir cpanel_deployment\backend 2>nul

echo Copying frontend build files...
xcopy frontend\build\* cpanel_deployment\frontend\ /E /Y

echo Copying backend files...
xcopy backend\* cpanel_deployment\backend\ /E /Y

echo.
echo Step 3: Creating .htaccess for frontend...
echo ^<IfModule mod_rewrite.c^> > cpanel_deployment\frontend\.htaccess
echo   RewriteEngine On >> cpanel_deployment\frontend\.htaccess
echo   RewriteBase / >> cpanel_deployment\frontend\.htaccess
echo   RewriteCond %%{REQUEST_FILENAME} !-f >> cpanel_deployment\frontend\.htaccess
echo   RewriteCond %%{REQUEST_FILENAME} !-d >> cpanel_deployment\frontend\.htaccess
echo   RewriteRule . /index.html [L] >> cpanel_deployment\frontend\.htaccess
echo ^</IfModule^> >> cpanel_deployment\frontend\.htaccess

echo.
echo Step 4: Creating Python app configuration...
echo import sys > cpanel_deployment\backend\passenger_wsgi.py
echo import os >> cpanel_deployment\backend\passenger_wsgi.py
echo sys.path.insert(0, os.path.dirname(__file__)) >> cpanel_deployment\backend\passenger_wsgi.py
echo from app.main import app >> cpanel_deployment\backend\passenger_wsgi.py
echo application = app >> cpanel_deployment\backend\passenger_wsgi.py

echo.
echo ========================================
echo    DEPLOYMENT PACKAGE READY!
echo ========================================
echo.
echo NEXT STEPS:
echo 1. Upload 'cpanel_deployment\frontend' contents to public_html
echo 2. Upload 'cpanel_deployment\backend' to a Python app folder
echo 3. Configure database in cPanel
echo 4. Set environment variables
echo.
echo Files ready in: cpanel_deployment\
echo.
pause