"""Generate an AutoHotkey v2 window switcher."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / 'GeneratedWindowsSwitcher.ahk'
HEADER = '''#Requires AutoHotkey v2.0
#SingleInstance Force
SetWorkingDir A_ScriptDir

ActivateClient(pid) {
    target := "ahk_pid " pid
    if WinExist(target) {
        try WinActivate(target)
    }
}
'''


def writeFile():
    OUTPUT.write_text(HEADER, encoding='utf-8')


def keybindBlock(pidList):
    pids = list(dict.fromkeys(int(str(pid).strip()) for pid in pidList if str(pid).strip()))
    if len(pids) > 36 or any(pid <= 0 for pid in pids):
        raise ValueError('Expected at most 36 positive client PIDs.')
    with OUTPUT.open('a', encoding='utf-8') as script:
        for index, pid in enumerate(pids):
            modifier = ('', '+', '^+')[index // 12]
            script.write(f'\n{modifier}F{index % 12 + 1}::ActivateClient({pid})\n')


def main():
    pids = (BASE_DIR / 'pidlist.txt').read_text(encoding='utf-8').splitlines()
    if not any(pid.strip() for pid in pids):
        raise ValueError('No clients found. Run pidCrawler.py after opening your clients.')
    writeFile()
    keybindBlock(pids)
    print(f'AutoHotkey v2 script created: {OUTPUT}')
    return True


if __name__ == '__main__':
    main()
