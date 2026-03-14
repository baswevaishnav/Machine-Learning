@echo off

REM Set the target project directory
SET PROJECT_DIR=C:\Users\VBaswe\Practice\Machine-Learning

REM Set log file location
SET LOG_FILE=%PROJECT_DIR%\setup_log.txt

REM Clear old log and start fresh
echo. > "%LOG_FILE%"

REM Helper: log to both screen and file
REM We'll use a simple approach - echo and append to log

echo ============================= 
echo  Python Virtual Environment Setup
echo =============================
echo ============================= >> "%LOG_FILE%"
echo  Python Virtual Environment Setup >> "%LOG_FILE%"
echo ============================= >> "%LOG_FILE%"

REM Log date and time
echo [INFO] Date: %DATE% >> "%LOG_FILE%"
echo [INFO] Time: %TIME% >> "%LOG_FILE%"
echo [INFO] Date: %DATE%
echo [INFO] Time: %TIME%
echo. >> "%LOG_FILE%"

REM Navigate to project directory
echo [STEP 1] Navigating to project directory...
echo [STEP 1] Navigating to project directory... >> "%LOG_FILE%"

cd /d "%PROJECT_DIR%"

IF ERRORLEVEL 1 (
    echo [FAILED] Directory not found: %PROJECT_DIR%
    echo [FAILED] Directory not found: %PROJECT_DIR% >> "%LOG_FILE%"
    echo [FAILED] Batch file stopped. >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo [OK] Now in: %PROJECT_DIR%
echo [OK] Now in: %PROJECT_DIR% >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Check and delete existing venv
echo [STEP 2] Checking for existing virtual environment...
echo [STEP 2] Checking for existing virtual environment... >> "%LOG_FILE%"

IF EXIST venv (
    echo [FOUND] Existing venv detected. Deleting...
    echo [FOUND] Existing venv detected. Deleting... >> "%LOG_FILE%"
    rmdir /s /q venv
    echo [OK] Old environment deleted.
    echo [OK] Old environment deleted. >> "%LOG_FILE%"
) ELSE (
    echo [INFO] No existing environment found.
    echo [INFO] No existing environment found. >> "%LOG_FILE%"
)
echo. >> "%LOG_FILE%"

REM Create new virtual environment
echo [STEP 3] Creating new virtual environment...
echo [STEP 3] Creating new virtual environment... >> "%LOG_FILE%"

py -m venv venv

IF ERRORLEVEL 1 (
    echo [FAILED] Could not create virtual environment. Is Python installed?
    echo [FAILED] Could not create virtual environment. Is Python installed? >> "%LOG_FILE%"
    echo [FAILED] Batch file stopped. >> "%LOG_FILE%"
    pause
    exit /b 1
)

echo [OK] Virtual environment created successfully.
echo [OK] Virtual environment created successfully. >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Activate the environment
echo [STEP 4] Activating virtual environment...
echo [STEP 4] Activating virtual environment... >> "%LOG_FILE%"

call "%PROJECT_DIR%\venv\Scripts\activate.bat"

echo [OK] Virtual environment is now ACTIVE.
echo [OK] Virtual environment is now ACTIVE. >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Log Python path
echo [STEP 5] Verifying Python path...
echo [STEP 5] Verifying Python path... >> "%LOG_FILE%"

FOR /F "tokens=*" %%i IN ('where python') DO (
    echo [OK] Python path: %%i
    echo [OK] Python path: %%i >> "%LOG_FILE%"
)
echo. >> "%LOG_FILE%"

REM Log installed packages
echo [STEP 6] Listing installed packages...
echo [STEP 6] Listing installed packages... >> "%LOG_FILE%"

pip list >> "%LOG_FILE%" 2>&1
pip list

echo. >> "%LOG_FILE%"
echo ============================= >> "%LOG_FILE%"
echo [SUCCESS] Setup completed: %DATE% %TIME% >> "%LOG_FILE%"
echo ============================= >> "%LOG_FILE%"

echo.
echo =============================
echo  Setup Complete! Happy Coding
echo =============================
echo.
echo [LOG] Log saved to: %LOG_FILE%
echo Open setup_log.txt in VS Code to review.
pause