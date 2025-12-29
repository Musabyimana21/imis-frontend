@echo off
echo ========================================
echo Python Installation Helper
echo ========================================
echo.

echo Checking for Python installation...
echo.

:: Check if Python is already installed
where python >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python is already installed!
    python --version
    echo.
    echo You can now run SETUP_CPANEL_DATABASE.bat
    goto :end
)

where py >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python is already installed!
    py --version
    echo.
    echo You can now run SETUP_CPANEL_DATABASE.bat
    goto :end
)

echo ❌ Python not found!
echo.
echo Choose installation method:
echo 1. Install from Microsoft Store (Recommended)
echo 2. Download from python.org
echo 3. Skip installation
echo.

set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo.
    echo Opening Microsoft Store...
    start ms-windows-store://pdp/?productid=9NCVDN91XZQP
    echo.
    echo After installation:
    echo 1. Close Microsoft Store
    echo 2. Run SETUP_CPANEL_DATABASE.bat again
) else if "%choice%"=="2" (
    echo.
    echo Opening python.org downloads...
    start https://python.org/downloads/
    echo.
    echo Installation instructions:
    echo 1. Download Python 3.11 or 3.12
    echo 2. Run the installer
    echo 3. ✅ CHECK "Add Python to PATH"
    echo 4. Complete installation
    echo 5. Run SETUP_CPANEL_DATABASE.bat again
) else (
    echo.
    echo Skipping installation.
    echo You can install Python later and run SETUP_CPANEL_DATABASE.bat
)

:end
echo.
pause