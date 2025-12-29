@echo off
echo ========================================
echo   IMIS Frontend Build for cPanel
echo ========================================

cd frontend

echo.
echo [1/4] Installing dependencies...
call npm install

echo.
echo [2/4] Building production frontend...
call npm run build

echo.
echo [3/4] Creating deployment package...
if exist "cpanel_deploy" rmdir /s /q cpanel_deploy
mkdir cpanel_deploy
xcopy /e /i /h /y build cpanel_deploy
xcopy /e /i /h /y dist cpanel_deploy 2>nul

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo   DEPLOYMENT INSTRUCTIONS:
echo ========================================
echo 1. Upload contents of 'frontend/cpanel_deploy/' to your cPanel public_html
echo 2. Or upload 'frontend/build/' or 'frontend/dist/' folder contents
echo 3. Make sure your backend is running on Render
echo 4. Test: https://e-shakiro.com
echo ========================================

pause