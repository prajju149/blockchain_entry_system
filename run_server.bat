@echo off
REM Run the blockchain entry system server
echo Starting Blockchain Entry System...
echo.
echo Server will start at http://127.0.0.1:5000
echo.
python wsgi.py
pause
