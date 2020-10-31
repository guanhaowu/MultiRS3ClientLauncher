import os
import sys
import clientLauncher
import pidCrawler
import fileWriter
import subprocess
import threading
import time
sys.path.insert(0, os.path.dirname(__file__))
# Count the arguments
userInput = sys.argv[1]


def main():
    x = threading.Thread(clientLauncher.run(userInput))
    x.start()
    x.join()
    time.sleep(5)
    pidCrawler.getPid()
    time.sleep(5)
    if (fileWriter.main()):
        subprocess.Popen(["C:\Program Files\AutoHotkey\AutoHotkey.exe", "GeneratedWindowsSwitcher.ahk"])
    exit()


if __name__ == "__main__":
    main()
