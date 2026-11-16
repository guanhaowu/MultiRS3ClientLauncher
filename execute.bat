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
Echo Open your clients manually through Jagex Launcher first. Sandboxie is optional.
Echo 1: Generate PID File.
Echo 2: Create AHK script.
Echo 3: Start AHK script.
Echo 4: Resize RuneScape windows using config.ini.
Echo 5: Stack RuneScape windows at monitor center using config.ini.
Echo 6: Exit.

choice /c 123456 /n /m "Choose an option: "
if errorlevel 255 goto response
if errorlevel 6 goto end
if errorlevel 5 goto StackWindows
if errorlevel 4 goto ResizeWindows
if errorlevel 3 goto StartAHKScript
if errorlevel 2 goto CreateAHKScript
if errorlevel 1 goto getPID
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

:ResizeWindows
"%PYTHON_EXE%" windowResizer.py
GOTO a

:StackWindows
"%PYTHON_EXE%" windowResizer.py --stack
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
