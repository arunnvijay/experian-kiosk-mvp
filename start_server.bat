@echo off
REM ============================================================================
REM Experian Kiosk MVP - Server Starter (Windows)
REM Purpose: Starts the FastAPI server on Windows
REM Usage: Double-click this file or run from command prompt
REM ============================================================================

echo.
echo ============================================================================
echo   EXPERIAN KIOSK MVP - STARTING SERVER
echo ============================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo.
    echo Please run setup_environment.bat first:
    echo   scripts\setup_environment.bat
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Check if backend exists
if not exist "backend\app.py" (
    echo [ERROR] backend\app.py not found!
    echo.
    echo Please ensure all MVP files are in place:
    echo   - backend\app.py
    echo   - backend\auth.py
    echo   - frontend\pages\index.html
    echo   - frontend\pages\dashboard.html
    echo   - frontend\pages\quiz.html
    echo.
    pause
    exit /b 1
)

REM Display server configuration
echo ============================================================================
echo   SERVER CONFIGURATION
echo ============================================================================
echo   Application:    Experian Kiosk MVP
echo   Framework:      FastAPI + Uvicorn
echo   Host:           127.0.0.1
echo   Port:           8000
echo   Authentication: Employee ID (U##### or ######)
echo ============================================================================
echo.

REM Display access information
echo ============================================================================
echo   ACCESS INFORMATION
echo ============================================================================
echo.
echo   Open your browser and navigate to:
echo.
echo     http://127.0.0.1:8000
echo     (or)
echo     http://localhost:8000
echo.
echo ============================================================================
echo   EMPLOYEE ID LOGIN
echo ============================================================================
echo.
echo   Valid formats:
echo     - U##### (e.g., U27214, U00001, U99999)
echo     - ###### (e.g., 123456, 000000, 999999)
echo.
echo   Test IDs available on the login page
echo.
echo ============================================================================
echo.
echo [INFO] Starting server...
echo [INFO] Press CTRL+C to stop the server
echo.
echo ============================================================================
echo.

REM Change to backend directory and start server
cd backend
python app.py

REM If server stops, show message
echo.
echo ============================================================================
echo   SERVER STOPPED
echo ============================================================================
echo.
echo The server has been stopped.
echo.
echo To start again, run: scripts\start_server.bat
echo.
pause
