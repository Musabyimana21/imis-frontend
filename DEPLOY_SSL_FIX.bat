@echo off
echo ========================================
echo RENDER SSL FIX DEPLOYMENT
echo ========================================
echo.
echo This will deploy the SSL fix to Render...
echo.

cd /d "f:\IMIS\backend"

echo Adding changes...
git add .

echo Committing SSL fix...
git commit -m "Fix: Enable SSL for PostgreSQL connections on Render"

echo Pushing to trigger Render deployment...
git push origin main

echo.
echo ========================================
echo DEPLOYMENT TRIGGERED
echo ========================================
echo.
echo Monitor your deployment at:
echo https://dashboard.render.com
echo.
echo Your app should be available at:
echo https://imis-backend-wk7z.onrender.com
echo.
pause