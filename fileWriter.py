import threading

def writeFile():
    print("Generating Initial AHK file...")
    f = open("GeneratedWindowsSwitcher.ahk", "w")
    f.writelines("""#SingleInstance force
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
""")
    f.close()


def keybindBlock(pidList):
    ClientNum = len(pidList)
    f1 = open("GeneratedWindowsSwitcher.ahk", "a")
    print("Generating Keybinds to file...")

    if ClientNum <= 12:
        for i in range(ClientNum):
            num = str(i + 1)
            text = "\n\nF" + num + ":: \n\t IfWinExist, ahk_class JagWindow \n\t\t WinActivate, ahk_pid " + pidList[
                i] + " \n\t return"
            f1.writelines(text)
    if ClientNum > 12 and ClientNum <= 24:
        for i in range(12,ClientNum):
            num = str(i + 1)
            text = "\n\n+F" + num + ":: \n\t IfWinExist, ahk_class JagWindow \n\t\t WinActivate, ahk_pid " + pidList[
                i] + " \n\t return"
            f1.writelines(text)
    if ClientNum > 24 and ClientNum <= 36:
        for i in range(24,ClientNum):
            num = str(i + 1)
            text = "\n\n^+F" + num + ":: \n\t IfWinExist, ahk_class JagWindow \n\t\t WinActivate, ahk_pid " + pidList[
                i] + " \n\t return"
            f1.writelines(text)
    f1.close()

def main():
    x = threading.Thread(writeFile())
    x.start()
    x.join()
    f = open("pidlist.txt")
    pidlist = f.readlines()
    f.close()
    y = threading.Thread(keybindBlock(pidlist))
    y.start()
    y.join()
    print("AHK Script file completed.")
    return True



if __name__ == '__main__':
    main()
