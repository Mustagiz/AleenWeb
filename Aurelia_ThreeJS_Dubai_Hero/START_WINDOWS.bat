@echo off
cd /d "%~dp0"
where node >nul 2>nul
if errorlevel 1 (
 echo Please install Node.js from https://nodejs.org then run this again.
 pause
 exit /b 1
)
call npm install
if errorlevel 1 (
 echo npm install failed. Check your internet connection.
 pause
 exit /b 1
)
call npm run dev
pause
