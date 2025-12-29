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

:: Copy frontend files (build)
echo Building and copying frontend...
cd frontend
call npm run build
cd ..
xcopy "frontend\build" "cpanel_deploy\frontend\" /E /I /Y

:: Create deployment instructions
echo Creating deployment instructions...
echo # IMIS cPanel Deployment Instructions > cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo. >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo ## Backend Deployment: >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo 1. Upload backend folder to public_html/api/ >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo 2. Install Python packages: pip install -r requirements.txt >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo 3. Set up Python app in cPanel pointing to app/main.py >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo. >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo ## Frontend Deployment: >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo 1. Upload frontend contents to public_html/ >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md
echo 2. Update API URLs to point to https://e-shakiro.com/api >> cpanel_deploy\DEPLOYMENT_INSTRUCTIONS.md

echo.
echo ✅ Deployment package created in 'cpanel_deploy' folder
echo.
echo Next steps:
echo 1. Compress cpanel_deploy folder to ZIP
echo 2. Upload to cPanel File Manager
echo 3. Follow DEPLOYMENT_INSTRUCTIONS.md
echo.
pause