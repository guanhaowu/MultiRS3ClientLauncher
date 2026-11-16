"""Resize currently visible RuneScape windows using config.ini."""
import configparser
import argparse
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


def setup_api():
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
    return user32


class MonitorInfo(ctypes.Structure):
    _fields_ = [('cbSize', wintypes.DWORD), ('rcMonitor', wintypes.RECT),
                ('rcWork', wintypes.RECT), ('dwFlags', wintypes.DWORD),
                ('szDevice', wintypes.WCHAR * 32)]


def get_monitors(user32):
    callback_type = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HANDLE,
                                      wintypes.HDC, ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)
    user32.EnumDisplayMonitors.argtypes = [wintypes.HDC, ctypes.POINTER(wintypes.RECT), callback_type, wintypes.LPARAM]
    user32.EnumDisplayMonitors.restype = wintypes.BOOL
    user32.GetMonitorInfoW.argtypes = [wintypes.HANDLE, ctypes.POINTER(MonitorInfo)]
    user32.GetMonitorInfoW.restype = wintypes.BOOL
    monitors = []
    errors = []

    @callback_type
    def collect(handle, _dc, _rect, _data):
        info = MonitorInfo()
        info.cbSize = ctypes.sizeof(info)
        if not user32.GetMonitorInfoW(handle, ctypes.byref(info)):
            errors.append(ctypes.get_last_error())
            return False
        work = info.rcWork
        monitors.append(dict(name=info.szDevice, primary=bool(info.dwFlags & 1),
                             area=(work.left, work.top, work.right, work.bottom)))
        return True

    if not user32.EnumDisplayMonitors(None, None, collect, 0) or errors:
        raise ctypes.WinError(errors[0] if errors else ctypes.get_last_error())
    return sorted(monitors, key=lambda monitor: monitor['name'])


def load_monitor(path=CONFIG):
    config = configparser.ConfigParser()
    with Path(path).open(encoding='utf-8') as source:
        config.read_file(source)
    return config.get('windows', 'monitor', fallback='primary').strip()


def center_position(monitors, selection, width, height):
    for monitor in monitors:
        short_name = monitor['name'].rsplit('\\', 1)[-1]
        if ((selection.casefold() == 'primary' and monitor['primary']) or
                selection.casefold() in (monitor['name'].casefold(), short_name.casefold())):
            left, top, right, bottom = monitor['area']
            if width > right - left or height > bottom - top:
                raise ValueError('Configured window size exceeds the selected monitor work area.')
            return left + (right - left - width) // 2, top + (bottom - top - height) // 2
    raise ValueError(f'Monitor {selection!r} not found. Run --list-monitors to see connected monitors.')


def resize_windows(width, height, stack=False, monitor='primary'):
    user32 = setup_api()
    x, y = center_position(get_monitors(user32), monitor, width, height) if stack else (0, 0)
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
        flags = 0x4014 if stack else 0x4016
        if user32.SetWindowPos(hwnd, None, x, y, width, height, flags):
            requested += 1
        else:
            error = ctypes.get_last_error()
            print(f'Could not resize client PID {pid}: {ctypes.FormatError(error)}')
    print(f'Requested {width} x {height} for {requested}/{len(windows)} window(s).')
    if stack:
        print(f'Stacked at ({x}, {y}) on monitor {monitor}.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stack', action='store_true', help='Resize and stack on the configured monitor')
    parser.add_argument('--list-monitors', action='store_true', help='List monitor names and usable desktop areas')
    args = parser.parse_args()
    try:
        if args.list_monitors:
            for monitor in get_monitors(setup_api()):
                label = ' (primary)' if monitor['primary'] else ''
                print(f"{monitor['name']}{label}: work area {monitor['area']}")
            return
        width, height = load_size()
        resize_windows(width, height, stack=args.stack, monitor=load_monitor() if args.stack else 'primary')
    except (OSError, ValueError, configparser.Error) as error:
        raise SystemExit(f'Window resize failed: {error}')


if __name__ == '__main__':
    main()
