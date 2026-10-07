@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Execute instalar_windows.bat primeiro.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" preparar_modelo.py
pause
