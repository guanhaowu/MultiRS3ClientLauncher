"""Generate and start a window switcher for already running clients."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import pidCrawler
import fileWriter


def find_ahk():
    """Find a v2 interpreter in per-user, system, or custom installs."""
    override = os.environ.get('AUTOHOTKEY_PATH')
    roots = []
    if os.name == 'nt':
        import winreg
        for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
            for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
                try:
                    with winreg.OpenKey(hive, r'SOFTWARE\AutoHotkey', 0, winreg.KEY_READ | view) as key:
                        roots.append(Path(winreg.QueryValueEx(key, 'InstallDir')[0]))
                except OSError:
                    pass
    if os.environ.get('LOCALAPPDATA'):
        roots.append(Path(os.environ['LOCALAPPDATA']) / 'Programs' / 'AutoHotkey')
    for variable in ('ProgramFiles', 'ProgramFiles(x86)'):
        if os.environ.get(variable):
            roots.append(Path(os.environ[variable]) / 'AutoHotkey')
    candidates = [root / 'v2' / name for root in roots for name in ('AutoHotkey64.exe', 'AutoHotkey32.exe')]
    candidates.extend(shutil.which(name) for name in ('AutoHotkey64.exe', 'AutoHotkey32.exe'))
    if override:
        candidates = [override]
    executable = next((str(p) for p in candidates if p and Path(p).is_file()), None)
    if not executable:
        raise FileNotFoundError('Install AutoHotkey v2 or set AUTOHOTKEY_PATH to its executable. The generated script is ready.')
    return executable


def start_ahk():
    executable = find_ahk()
    subprocess.Popen([executable, str(fileWriter.OUTPUT)], cwd=fileWriter.BASE_DIR)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--start-ahk', action='store_true')
    args = parser.parse_args()
    if args.start_ahk:
        start_ahk()
        return
    pidCrawler.getPid()
    fileWriter.main()
    start_ahk()


if __name__ == '__main__':
    main()
