"""Find RS3 processes and Sandboxie-renamed game windows."""
import ctypes
from ctypes import wintypes
from pathlib import Path
import psutil

BASE_DIR = Path(__file__).resolve().parent


def findProcessIdByName(processName):
    results = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if processName.lower() in (proc.info['name'] or '').lower():
                try:
                    created = proc.create_time()
                except psutil.Error:
                    created = 0
                results.append(dict(proc.info, create_time=created))
        except psutil.Error:
            continue
    return results


def checkIfProcessRunning(processName):
    return bool(findProcessIdByName(processName))


def findWindows(process_pids=()):
    """Return visible game windows as (HWND, PID) pairs."""
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    user32.EnumWindows.argtypes = [callback_type, wintypes.LPARAM]
    user32.EnumWindows.restype = wintypes.BOOL
    user32.IsWindowVisible.argtypes = [wintypes.HWND]
    user32.GetClassNameW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    user32.GetWindowThreadProcessId.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
    windows = []
    process_pids = set(process_pids)

    @callback_type
    def collect(hwnd, _):
        name = ctypes.create_unicode_buffer(512)
        if user32.IsWindowVisible(hwnd) and user32.GetClassNameW(hwnd, name, len(name)):
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value and (name.value.casefold().split(':')[-1] == 'jagwindow' or pid.value in process_pids):
                windows.append((hwnd, pid.value))
        return True

    if not user32.EnumWindows(collect, 0):
        raise ctypes.WinError(ctypes.get_last_error())
    return windows


def findWindowPids():
    return {pid for _, pid in findWindows()}


def getPid():
    processes = {p['pid']: p for p in findProcessIdByName('rs2client')}
    for pid in findWindowPids():
        if pid not in processes:
            try:
                created = psutil.Process(pid).create_time()
            except psutil.Error:
                created = 0
            processes[pid] = dict(pid=pid, create_time=created)
    ordered = sorted(processes.values(), key=lambda p: (p['create_time'], p['pid']))
    pids = [p['pid'] for p in ordered]
    (BASE_DIR / 'pidlist.txt').write_text(''.join(f'{pid}\n' for pid in pids), encoding='utf-8')
    print(f'Found {len(pids)} RuneScape client(s): {pids}')
    if not pids:
        print('Run this tool outside Sandboxie, on the same Windows desktop as the clients.')
    return pids


if __name__ == '__main__':
    getPid()
