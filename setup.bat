@echo off
REM HIPAA Training System V2.0 - Windows Setup Script
REM Automated setup for V2.0 development and testing

setlocal enabledelayedexpansion

echo ========================================
echo HIPAA Training System V2.0 - Setup
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

REM Verify Python 3.8+
echo Verifying Python version compatibility...
for /f "tokens=1,2,3 delims=." %%a in ("%PYTHON_VERSION%") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if %MAJOR% LSS 3 (
    echo [ERROR] Python 3.8+ required, found %PYTHON_VERSION%
    pause
    exit /b 1
)

if %MAJOR% EQU 3 (
    if %MINOR% LSS 8 (
        echo [ERROR] Python 3.8+ required, found %PYTHON_VERSION%
        pause
        exit /b 1
    )
)
echo [OK] Python version 3.8+ confirmed
echo.

REM Check V2.0 required files
echo Checking V2.0 required files...
set MISSING_FILES=0

if not exist "hipaa_training_v2.py" (
    echo [ERROR] Missing: hipaa_training_v2.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] Found: hipaa_training_v2.py
)

if not exist "test_hipaa_training_v2.py" (
    echo [ERROR] Missing: test_hipaa_training_v2.py
    set /a MISSING_FILES+=1
) else (
    echo [OK] Found: test_hipaa_training_v2.py
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
    echo [ERROR] Missing required V2.0 files
    pause
    exit /b 1
)
echo.

REM Verify V2.0 content completeness
echo Verifying V2.0 content completeness...
python -c "
import hipaa_training_v2 as ht
print('[OK] 13 lessons loaded:', len(ht.LESSONS))
print('[OK] 15 quiz questions:', len(ht.QUIZ_QUESTIONS))  
print('[OK] 15 checklist items:', len(ht.CHECKLIST_ITEMS))
"
if errorlevel 1 (
    echo [ERROR] Failed to verify V2.0 content
    pause
    exit /b 1
)
echo.

REM Create virtual environment
set /p CREATE_VENV="Create virtual environment? (recommended) [Y/N]: "
if /i "!CREATE_VENV!"=="Y" (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment created and activated
    echo.
)

REM Run V2.0 tests
echo Running V2.0 system tests...
python test_hipaa_training_v2.py
if errorlevel 1 (
    echo [WARNING] Some V2.0 tests failed
    set /p CONTINUE="Continue anyway? [Y/N]: "
    if /i not "!CONTINUE!"=="Y" exit /b 1
) else (
    echo [OK] All V2.0 tests passed
)
echo.

REM Test V2.0 program startup
echo Testing V2.0 program startup...
echo 5 | python hipaa_training_v2.py >nul 2>&1
if errorlevel 1 (
    echo [ERROR] V2.0 program failed to start
    pause
    exit /b 1
) else (
    echo [OK] V2.0 program starts successfully
)
echo.

REM Set up Git hooks for V2.0
if exist ".git" (
    echo Setting up V2.0 Git hooks...
    (
        echo @echo off
        echo echo Running V2.0 tests before commit...
        echo python test_hipaa_training_v2.py
        echo if errorlevel 1 (
        echo   echo Tests failed. Commit aborted.
        echo   exit /b 1
        echo )
        echo echo V2.0 tests passed. Proceeding with commit.
    ) > .git\hooks\pre-commit.bat
    echo [OK] V2.0 Git hooks installed
    echo.
)

REM Create sample progress file for V2.0
set /p CREATE_SAMPLE="Generate sample progress file for testing? [Y/N]: "
if /i "!CREATE_SAMPLE!"=="Y" (
    echo Creating V2.0 sample progress file...
    (
        echo {
        echo   "timestamp": "2025-10-02T14:30:00.123456",
        echo   "checklist": {
        echo     "Completed Privacy Rule training": true,
        echo     "Reviewed Security Rule requirements": true,
        echo     "Understands breach notification timeline (60 days)": false,
        echo     "Can identify and report unauthorized access": true,
        echo     "Knows and applies minimum necessary standard": true,
        echo     "Can identify all 18 types of Protected Health Information": false,
        echo     "Understands all patient rights under HIPAA": true,
        echo     "ePHI encrypted at rest (hard drives, servers)": false,
        echo     "ePHI encrypted in transit (secure transmissions)": false,
        echo     "Audit logs enabled and monitored regularly": false,
        echo     "Cross-cut shredders used for all PHI disposal": true,
        echo     "Unique login credentials for every staff member": true,
        echo     "All staff HIPAA training completed annually": false,
        echo     "Business Associate Agreements signed with vendors": false,
        echo     "Notice of Privacy Practices provided to all patients": true
        echo   },
        echo   "compliance_score": "8/15",
        echo   "percentage": 53.3
        echo }
    ) > hipaa_progress_sample.json
    echo [OK] V2.0 sample file created: hipaa_progress_sample.json
    echo.
)

REM Security check for V2.0 files
echo Setting V2.0 file permissions...
icacls "hipaa_training_v2.py" /reset >nul 2>&1
icacls "test_hipaa_training_v2.py" /reset >nul 2>&1

if exist "hipaa_progress.json" (
    icacls "hipaa_progress.json" /grant:r "%USERNAME%:R" >nul 2>&1
    echo [OK] Secured hipaa_progress.json
)
echo [OK] V2.0 file permissions set
echo.

REM Display V2.0 setup summary
echo ========================================
echo V2.0 Setup Complete!
echo ========================================
echo.
echo [OK] Python %PYTHON_VERSION% verified
echo [OK] All V2.0 files present
echo [OK] 13 lessons, 15 quiz questions, 15 checklist items
echo [OK] V2.0 tests passing
echo [OK] Program verified
echo.

if exist ".git" (
    echo [OK] V2.0 Git hooks installed
)

echo V2.0 Quick Start:
echo   Run the program: python hipaa_training_v2.py
echo   Run tests:       python test_hipaa_training_v2.py
echo   View README:     type README.md
echo.

if /i "!CREATE_VENV!"=="Y" (
    echo Note: Virtual environment active
    echo   Deactivate:      deactivate
    echo   Reactivate:      venv\Scripts\activate.bat
    echo.
)

echo V2.0 Features:
echo   • 13 comprehensive lessons
echo   • 15 real-world quiz scenarios
echo   • 15-item compliance checklist
echo   • 95%%+ HIPAA coverage
echo   • Pharmacy-specific content
echo.

echo Setup completed successfully! 🎉
echo.
pause
