@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Execute instalar_windows.bat primeiro.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" main.py
if errorlevel 1 (
    echo.
    echo O programa terminou com erro. Confira a mensagem acima.
    pause
)
