@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
echo Ambiente Python nao encontrado.
echo Execute primeiro: python -m venv .venv
pause
exit /b 1
)
".venv\Scripts\python.exe" "src\main.py"
pause