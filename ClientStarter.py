import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import pidCrawler
import fileWriter
import subprocess
import threading
import time

# Count the arguments
userInput = sys.argv[1]


def startClient():
    rsPath = r"C:\Program Files\Jagex\RuneScape Launcher\RuneScape.exe"
    subprocess.Popen(rsPath)


def runClient(x):
    i = 0
    AClient = int(x)
    while i < AClient:
        print("Starting client " + str(i + 1) + "...")
        x = threading.Thread(startClient())
        x.start()
        i += 1
    x.join()


def main():
    status = False
    AmountClient = int(userInput)
    if AmountClient >0 and AmountClient <= 36:
        _AmountClient1 = (AmountClient // 5)
        _AmountClient2 = (AmountClient % 5)
        for i in range(_AmountClient1):
            runClient(5)
            time.sleep(3)

        if _AmountClient2>0:
            runClient(_AmountClient2)
            time.sleep(3)
            status = True
        else:
            status = True

        if status:
            time.sleep(5)
            x = threading.Thread(pidCrawler.getPid())
            x.start()
            x.join()
            fileWriter.main()
    exit()


if __name__ == "__main__":
    main()
