@echo off
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
START CMD @cmd /c "call py -3.7 script.py %clients%"
GOTO a

:LaunchClient
Echo [Starting client launcher...]
set "clients=default 0"
set /p clients="Enter amount of clients (max 36): "
Echo [input: %clients%]
Echo [End of Starting Launchers]
IF "%clients%" == "0" GOTO warn_no_client
START CMD @cmd /c "call py -3.7 clientLauncher.py %clients%"
GOTO a

:getPID
Echo [Generating PID list with all RS3 Clients.]
START CMD @cmd /c "call py -3.7 pidCrawler.py
Echo [Task completed, returning to options menu...]
timeout 2
GOTO a

:CreateAHKScript
Echo [Generating AHK script with all RS3 Clients PID...]
START CMD @cmd /c "call py -3.7 fileWriter.py
Echo [Task completed, returning to options menu...]
timeout 2
GOTO a

:StartAHKScript
Echo [Starting AHK script...]
START GeneratedWindowsSwitcher.ahk
Echo [Task completed, returning to options menu...]
timeout 2
GOTO a

:warn_no_client
Echo [No number of clients in input found.]
GOTO a

:response
Echo [Invalid option, returning back to menu option.]
timeout 2
GOTO a

:end
Echo [Closing script.]
timeout 1
exit