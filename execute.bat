@echo off
Echo Starting Launchers
set "clients=default 0"
set /p clients="Enter amount of clients (max 36): "
Echo input: %clients%
Echo End of Starting Launchers
IF "%clients%" == "0" GOTO end
START CMD @cmd /c "call py -3.7 ClientStarter.py %clients%"
Echo Closing script.
timeout 3
exit

:end
Echo No number of clients in input found.
Echo Closing script.
timeout 5
exit