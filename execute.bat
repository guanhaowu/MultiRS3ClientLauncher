@echo off
cd /d "%~dp0"
call :findPython
if not defined PYTHON_EXE (
    echo No working Python 3.10+ installation found. Install Python from python.org.
    pause
    exit /b 1
)
echo Using "%PYTHON_EXE%"
GOTO a
:a
Echo Choose an option:
Echo 1: Start everything.
Echo 2: Launch RS3 Clients.
Echo 3: Generate PID File.
Echo 4: Create AHK script.
Echo 5: Start AHK script.
Echo 6: Exit.

set /p OPTIONS="Choose an option: "
IF %OPTIONS% == 0 GOTO response
IF %OPTIONS% == 1 GOTO everything
IF %OPTIONS% == 2 GOTO LaunchClient
IF %OPTIONS% == 3 GOTO getPID
IF %OPTIONS% == 4 GOTO CreateAHKScript
IF %OPTIONS% == 5 GOTO StartAHKScript
IF %OPTIONS% == 6 GOTO end
IF %OPTIONS% geq 7 GOTO response
GOTO a

:everything
Echo Starting Script
set "clients=default 0"
set /p clients="Enter amount of clients (max 36): "
Echo [input: %clients%]
Echo [End of Starting Launchers]
IF "%clients%" == "0" GOTO warn_no_client
"%PYTHON_EXE%" script.py %clients%
GOTO a

:LaunchClient
Echo [Starting client launcher...]
set "clients=default 0"
set /p clients="Enter amount of clients (max 36): "
Echo [input: %clients%]
Echo [End of Starting Launchers]
IF "%clients%" == "0" GOTO warn_no_client
"%PYTHON_EXE%" clientLauncher.py %clients%
GOTO a

:getPID
Echo [Generating PID list with all RS3 Clients.]
"%PYTHON_EXE%" pidCrawler.py
Echo [Task completed, returning to options menu...]
C:\windows\system32\timeout /t 2
GOTO a

:CreateAHKScript
Echo [Generating AHK script with all RS3 Clients PID...]
"%PYTHON_EXE%" fileWriter.py
Echo [Task completed, returning to options menu...]
C:\windows\system32\timeout /t 2
GOTO a

:StartAHKScript
Echo [Starting AHK script...]
"%PYTHON_EXE%" script.py --start-ahk
Echo [Task completed, returning to options menu...]
C:\windows\system32\timeout /t 2
GOTO a

:warn_no_client
Echo [No number of clients in input found.]
GOTO a

:response
Echo [Invalid option, returning back to menu option.]
C:\windows\system32\timeout /t 2
GOTO a

:end
Echo [Closing script.]
C:\windows\system32\timeout /t 1
exit /b

:findPython
if defined PYTHON_EXE (
    call :checkPython "%PYTHON_EXE%"
    if not errorlevel 1 exit /b
)
set "PYTHON_EXE="
for %%P in ("%~dp0.venv\Scripts\python.exe") do (
    if exist "%%~P" (
        call :checkPython "%%~P"
        if not errorlevel 1 (
            set "PYTHON_EXE=%%~P"
            exit /b
        )
    )
)
for /d %%D in ("%ProgramFiles%\Python*" "%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%~D\python.exe" (
        call :checkPython "%%~D\python.exe"
        if not errorlevel 1 (
            set "PYTHON_EXE=%%~D\python.exe"
            exit /b
        )
    )
)
for /f "delims=" %%P in ('where python.exe 2^>nul') do (
    echo %%P | findstr /i /c:"\WindowsApps\" >nul
    if errorlevel 1 (
        call :checkPython "%%P"
        if not errorlevel 1 (
            set "PYTHON_EXE=%%P"
            exit /b
        )
    )
)
exit /b

:checkPython
"%~1" -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
exit /b %errorlevel%
