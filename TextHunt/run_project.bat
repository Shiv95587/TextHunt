@echo off
echo Starting the application...

:: Start the Flask backend (assuming the app.exe is in the root folder)
start app.exe

:: Wait a few seconds to ensure the server is up
timeout 5

:: Open the browser to the React frontend
start http://localhost:5000

pause
 