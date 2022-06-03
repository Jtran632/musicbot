@echo off 
setlocal enabledelayedexpansion
COLOR 0f
if not "%1" == "max" start /MAX cmd /c %0 max & exit/b
echo Press any key to install required files for bot
pause >nul
pip install -r requirements.txt
TIMEOUT /T 3 > NUL
pause