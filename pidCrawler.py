import os
import sys
import psutil
import time

sys.path.insert(0, os.path.dirname(__file__))

# Script from somewhere on the internet to get list of Process, PID and name

"""
Check if there is any running process that contains the given name processName.
"""


def checkIfProcessRunning(processName):
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


"""
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
"""


def findProcessIdByName(processName):
    listOfProcessObjects = []

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            procInfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if processName.lower() in procInfo['name'].lower():
                listOfProcessObjects.append(procInfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return listOfProcessObjects


def getPid():
    print("*** Check if a process is running or not ***")

    # Check if any chrome process was running or not.
    if checkIfProcessRunning('rs2client'):
        print('rs2client process is running')
    else:
        print('No rs2client process is running')

    print("*** Find PIDs of a running process by Name ***")

    # Find PIDs od all the running instances of process that contains 'rs2client' in its name
    listOfProcessIds = findProcessIdByName('rs2client')

    listOfResults = []
    if len(listOfProcessIds) > 0:
        print('Process Exists | PID and other details are')
        for elem in listOfProcessIds:
            processCreationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(elem['create_time']))
            processID = elem['pid']
            processName = elem['name']
            listOfResults.append((processCreationTime, processID, processName))

    listOfResult = sorted(listOfResults)
    f = open("pidlist.txt", "w+")
    print("Making pid list file...")
    for el in listOfResult:
        print(el)
        text = str(el[1]) + "\n"
        f.write(text)
    print("Pid list file created...")
    f.close()
    return


if __name__ == "__main__":
    getPid()
