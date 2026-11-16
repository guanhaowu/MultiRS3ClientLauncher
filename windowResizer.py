"""Resize currently visible RuneScape windows using config.ini."""
import configparser
import ctypes
from ctypes import wintypes
from pathlib import Path

import pidCrawler

CONFIG = Path(__file__).resolve().with_name('config.ini')


def load_size(path=CONFIG):
    config = configparser.ConfigParser()
    with Path(path).open(encoding='utf-8') as source:
        config.read_file(source)
    width = config.getint('windows', 'width')
    height = config.getint('windows', 'height')
    if not (1 <= width <= 32767 and 1 <= height <= 32767):
        raise ValueError('Width and height must be integers between 1 and 32767.')
    return width, height


def resize_windows(width, height):
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    # Request physical pixel sizing on displays with scaling enabled.
    try:
        user32.SetProcessDpiAwarenessContext.argtypes = [ctypes.c_void_p]
        user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except AttributeError:
        user32.SetProcessDPIAware()
    user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, ctypes.c_int,
                                  ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.UINT]
    user32.SetWindowPos.restype = wintypes.BOOL
    user32.ShowWindowAsync.argtypes = [wintypes.HWND, ctypes.c_int]
    user32.IsIconic.argtypes = [wintypes.HWND]
    user32.IsZoomed.argtypes = [wintypes.HWND]
    processes = pidCrawler.findProcessIdByName('rs2client')
    windows = pidCrawler.findWindows(p['pid'] for p in processes)
    if not windows:
        print('No RuneScape windows found. Open your clients first and run this tool outside Sandboxie.')
        return
    requested = 0
    for hwnd, pid in windows:
        # Restore minimized/maximized windows before setting their normal size.
        if user32.IsIconic(hwnd) or user32.IsZoomed(hwnd):
            user32.ShowWindowAsync(hwnd, 9)
        # NOMOVE | NOZORDER | NOACTIVATE | ASYNCWINDOWPOS: preserve placement
        # and avoid blocking on an unresponsive client.
        if user32.SetWindowPos(hwnd, None, 0, 0, width, height, 0x4016):
            requested += 1
        else:
            error = ctypes.get_last_error()
            print(f'Could not resize client PID {pid}: {ctypes.FormatError(error)}')
    print(f'Requested {width} x {height} for {requested}/{len(windows)} window(s).')


def main():
    try:
        width, height = load_size()
        resize_windows(width, height)
    except (OSError, ValueError, configparser.Error) as error:
        raise SystemExit(f'Window resize failed: {error}')


if __name__ == '__main__':
    main()
