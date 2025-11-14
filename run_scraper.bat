@echo off
setlocal

:: Set the title of the window
title GitHub Mail Scraper

:: --- Configuration ---
:: 1. Make sure Python is installed and in your PATH.
:: 2. Create a file named token.txt in this directory and paste your GitHub token into it.
set TOKEN_FILE=token.txt
set PYTHON_CMD=python

:: --- Pre-flight Checks ---
echo Checking for Python...
%PYTHON_CMD% --version >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python is not found in your PATH.
    echo Please install Python and make sure it's added to your PATH.
    pause
    exit /b 1
)

echo Checking for token file (%TOKEN_FILE%)...
if not exist "%TOKEN_FILE%" (
    echo Error: %TOKEN_FILE% not found.
    echo Please create this file and paste your GitHub token into it.
    pause
    exit /b 1
)

:: Read token from file
set /p GITHUB_TOKEN=<%TOKEN_FILE%
if not defined GITHUB_TOKEN (
    echo Error: Could not read token from %TOKEN_FILE%. Make sure it's not empty.
    pause
    exit /b 1
)

echo Token loaded successfully.

echo.
echo Installing/checking required Python packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install requirements.
    pause
    exit /b 1
)
echo Packages are up to date.
echo.

:: --- Main Loop ---
echo Starting continuous scraping in random mode...
echo Press Ctrl+C to stop the process.
echo.

:loop
echo -------------------------------------------------
echo [%time%] Starting new auto-fetch cycle...
echo -------------------------------------------------
set PYTHONPATH=src
%PYTHON_CMD% -m scraper.cli auto-fetch --mode random --token %GITHUB_TOKEN%

echo.
echo Cycle finished. Waiting 10 seconds before starting the next one...
timeout /t 10 /nobreak
goto loop

endlocal
