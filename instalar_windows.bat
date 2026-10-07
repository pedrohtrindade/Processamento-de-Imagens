@echo off
setlocal
cd /d "%~dp0"
echo Instalando o projeto em um ambiente isolado...
if exist ".venv\Scripts\python.exe" goto dependencias
py -3.11 -c "import sys" >nul 2>&1
if not errorlevel 1 (
    py -3.11 -m venv .venv
) else (
    py -3.12 -c "import sys" >nul 2>&1
    if errorlevel 1 (
        echo Instale Python 3.11 ou 3.12 de 64 bits em python.org, incluindo o Python Launcher.
        echo Depois execute este arquivo novamente.
        pause
        exit /b 1
    )
    py -3.12 -m venv .venv
)
if not exist ".venv\Scripts\python.exe" (
    echo Falha ao criar o ambiente Python.
    pause
    exit /b 1
)
:dependencias
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto falha
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto falha
rem Ultralytics exige opencv-python. Reinstalar contrib por ultimo garante CSRT.
".venv\Scripts\python.exe" -m pip install --force-reinstall --no-deps opencv-contrib-python==4.11.0.86
if errorlevel 1 goto falha
".venv\Scripts\python.exe" -c "import cv2; assert hasattr(cv2, 'TrackerCSRT_create'), 'CSRT indisponivel'"
if errorlevel 1 goto falha
echo.
echo Instalacao concluida. Use iniciar_windows.bat para abrir o programa.
echo Antes da apresentacao, use baixar_modelo_windows.bat com acesso a internet.
pause
exit /b 0
:falha
echo.
echo A instalacao falhou. Confira a mensagem acima e sua conexao com a internet.
pause
exit /b 1
