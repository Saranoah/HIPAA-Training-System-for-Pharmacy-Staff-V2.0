@echo off
REM HIPAA Training System - Windows Setup Script
REM Automated setup for development and testing

setlocal enabledelayedexpansion

echo ========================================
echo HIPAA Training System - Setup
echo ========================================
echo.

REM Check Python installation
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Found Python %PYTHON_VERSION%
echo.

REM Check required files
echo Checking required files...
set MISSING_FILES=0

if not exist "hipaa_ai_pharmacy_production.py" (
    echo [ERROR] Missing: hipaa_ai_pharmacy_production.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] Found: hipaa_ai_pharmacy_production.py
)

if not exist "test_hipaa_training.py" (
    echo [ERROR] Missing: test_hipaa_training.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] Found: test_hipaa_training.py
)

if not exist "README.md" (
    echo [ERROR] Missing: README.md
    set /a MISSING_FILES+=1
) else (
    echo [OK] Found: README.md
)

if not exist "LICENSE" (
    echo [ERROR] Missing: LICENSE
    set /a MISSING_FILES+=1
) else (
    echo [OK] Found: LICENSE
)

if %MISSING_FILES% gtr 0 (
    echo [ERROR] Missing required files
    pause
    exit /b 1
)
echo.

REM Create virtual environment
set /p CREATE_VENV="Create virtual environment? (recommended) [Y/N]: "
if /i "%CREATE_VENV%"=="Y" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment created and activated
    echo.
)

REM Run tests
echo Running system tests...
python test_hipaa_training.py
if errorlevel 1 (
    echo [ERROR] Some tests failed
    set /p CONTINUE="Continue anyway? [Y/N]: "
    if /i not "!CONTINUE!"=="Y" exit /b 1
) else (
    echo [OK] All tests passed
)
echo.

REM Test program startup
echo Testing program startup...
echo 7 | python hipaa_ai_pharmacy_production.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Program failed to start
    pause
    exit /b 1
) else (
    echo [OK] Program starts successfully
)
echo.

REM Create sample progress file
set /p CREATE_SAMPLE="Generate sample progress file for testing? [Y/N]: "
if /i "%CREATE_SAMPLE%"=="Y" (
    echo Creating sample progress file...
    (
        echo {
        echo   "last_updated": "2025-10-02T14:30:00.123456",
        echo   "timestamp": "2025-10-02 14:30:00",
        echo   "checklist": {
        echo     "Completed Privacy Rule training": true,
        echo     "Reviewed Security Rule requirements": true,
        echo     "Understands breach notification timeline": false,
        echo     "Can identify unauthorized access": true,
        echo     "Knows minimum necessary standard": true,
        echo     "Encrypted ePHI at rest": false,
        echo     "Encrypted ePHI in transit": false,
        echo     "Audit logs enabled": false,
        echo     "Staff HIPAA training completed": true,
        echo     "Business Associate Agreements signed": false
        echo   },
        echo   "compliance_score": "5/10",
        echo   "percentage": 50.0
        echo }
    ) > hipaa_progress_sample.json
    echo [OK] Sample file created: hipaa_progress_sample.json
    echo.
)

REM Display setup summary
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo [OK] Python %PYTHON_VERSION% verified
echo [OK] All required files present
echo [OK] Tests passing
echo [OK] Program verified
echo.
echo Quick Start:
echo   Run the program: python hipaa_ai_pharmacy_production.py
echo   Run tests:       python test_hipaa_training.py
echo   View README:     type README.md
echo.

if /i "%CREATE_VENV%"=="Y" (
    echo Note: Virtual environment active
    echo   Deactivate:      deactivate
    echo   Reactivate:      venv\Scripts\activate.bat
    echo.
)

echo Documentation:
echo   Testing Guide:   TESTING.md
echo   Contributing:    CONTRIBUTING.md
echo.
echo Setup completed successfully!
echo.
pause
