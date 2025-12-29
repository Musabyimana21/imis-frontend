@echo off
echo ========================================
echo IMIS cPanel Database Setup
echo ========================================
echo.

cd /d "%~dp0"

echo Checking for Python installation...
echo.

:: Try different Python commands
where python >nul 2>&1
if %errorlevel% == 0 (
    echo Found: python
    python setup_cpanel_db.py
    goto :end
)

where py >nul 2>&1
if %errorlevel% == 0 (
    echo Found: py
    py setup_cpanel_db.py
    goto :end
)

where python3 >nul 2>&1
if %errorlevel% == 0 (
    echo Found: python3
    python3 setup_cpanel_db.py
    goto :end
)

echo ❌ Python not found!
echo.
echo Please install Python:
echo 1. Open Microsoft Store
echo 2. Search for "Python 3.12"
echo 3. Install Python
echo 4. Run this script again
echo.
echo Or download from: https://python.org/downloads/
echo (Make sure to check "Add Python to PATH")

:end
echo.
pause
