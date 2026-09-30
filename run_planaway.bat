@echo off
title PlanAway - AI Travel Recommendation System
color 0A
echo ============================================================
echo           PLANAWAY - AI TRAVEL RECOMMENDATION SYSTEM
echo ============================================================
echo.
cd /d "%~dp0"

echo [1/3] Detecting Python environment...
set PYTHON_CMD=python

where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% eq 0 (
        set PYTHON_CMD=py
    ) else (
        echo ERROR: Python is not installed or not added to PATH!
        echo Please install Python from https://www.python.org/ and check 'Add Python to PATH'.
        echo.
        pause
        exit /b 1
    )
)

echo Using command: %PYTHON_CMD%
echo.

echo [2/3] Checking ML Model artifacts...
if not exist model.pkl (
    echo Model file model.pkl not found. Training model now...
    %PYTHON_CMD% train_model.py
) else (
    echo Machine Learning Model (model.pkl) is ready!
)

echo.
echo ============================================================
echo [3/3] Starting PlanAway Web Server...
echo Server running at: http://127.0.0.1:5000
echo Opening web browser automatically...
echo (Keep this command window open while using the website)
echo ============================================================
echo.

start http://127.0.0.1:5000

%PYTHON_CMD% app.py

echo.
echo Server stopped.
pause
