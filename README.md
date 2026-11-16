# MultiRS3ClientLauncher

A Windows utility that discovers running RuneScape 3 clients and generates an
AutoHotkey v2 script to focus each client with a keyboard shortcut. Supports up
to 36 clients, including clients already running in Sandboxie.

## Requirements

| Requirement | Purpose |
| --- | --- |
| Windows 10 or 11 | Process discovery and window switching use Windows APIs. |
| [Python](https://www.python.org/downloads/windows/) 3.10 or newer | Runs the Python tools and batch menu. |
| pip and Python's `venv` module | Installs dependencies into a project environment. Included with standard Python installations. |
| `psutil>=5.9` | The only third-party Python dependency; listed in `requirements.txt`. |
| [AutoHotkey v2](https://www.autohotkey.com/) | Runs the generated window-switching script. AutoHotkey v1 cannot run it. |
| RuneScape 3 and access to your game accounts | Open the clients before generating shortcuts, or configure a directly launchable client executable. |
| [Sandboxie Plus or Classic](https://sandboxie-plus.com/) (optional) | Only needed if you want to run your game clients in sandboxes. |

Keep all project files together in a writable folder. Internet access is needed
for downloads and dependency installation. The switcher does not require an API
key, a Python IDE, or additional Python packages.

## First-time setup

1. Download or clone this repository and extract it to a writable folder.
2. Install Python 3.10 or newer. Enable the installer option to add Python to PATH
   if offered, or use the full path to `python.exe` below.
3. Install AutoHotkey **v2**. A per-user installation is supported, and v1 may
   remain installed alongside v2.
4. Open PowerShell in the project folder and create the Python environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

If `python` displays the Microsoft Store message, use the actual installed
executable to create the environment. For example, if installed at this path:

```powershell
& 'C:\Program Files\Python314\python.exe' -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Adjust the installation path for your machine. Environment activation and a
PowerShell execution-policy change are unnecessary: the commands below call
the environment's executable directly.

## Use existing clients, including Sandboxie clients

1. Open your RuneScape 3 clients through your usual launcher or Sandboxie.
2. Wait for their game windows to appear.
3. Run this tool **outside Sandboxie**, on the same Windows desktop and user
   session as the clients.
4. Run:

```powershell
.\.venv\Scripts\python.exe script.py
```

This discovers clients, writes `pidlist.txt`, generates
`GeneratedWindowsSwitcher.ahk`, and starts it with AutoHotkey v2.

Alternatively, double-click `execute.bat`, then choose **3**, **4**, and **5** in
that order. The menu finds the project's `.venv` automatically, then searches
standard Python installation folders and PATH, skipping Windows Store aliases.

Discovery combines `rs2client` process-name matching with visible `JagWindow`
windows, including Sandboxie-renamed window classes. Switching targets each
process ID (PID), without requiring an exact window class or title.

Regenerate and restart the script whenever clients are restarted, added, or
removed. PIDs change between runs. The script does not automatically refresh its
client list. Clients are normally ordered by process creation time, with PID as
an additional sort key; clients with inaccessible creation times sort first.

## Keyboard shortcuts

| Clients | Shortcuts |
| --- | --- |
| 1-12 | F1-F12 |
| 13-24 | Shift+F1-Shift+F12 |
| 25-36 | Ctrl+Shift+F1-Ctrl+Shift+F12 |

These shortcuts are global while the generated script is running. Each shortcut
focuses one client window. Exit the script through the AutoHotkey tray icon to
release the shortcuts. Starting the generated script again replaces its previous
instance. Closing the batch menu does not stop the AutoHotkey script.

## Batch menu

| Option | Action |
| --- | --- |
| 1 | Launch 1-36 clients, discover clients, generate shortcuts, and start AutoHotkey. |
| 2 | Launch 1-36 clients only. |
| 3 | Discover running clients and write `pidlist.txt`. |
| 4 | Generate the AutoHotkey v2 script from `pidlist.txt`. |
| 5 | Start the previously generated AutoHotkey script. |
| 6 | Close the menu. |

For clients already running in Sandboxie, use options **3 -> 4 -> 5**.
Options 1 and 2 launch ordinary clients; sandbox selection and sandboxed launching
remain manual steps. Option 5 does not refresh the saved client list.

## Individual commands

Run these from the project folder in PowerShell:

```powershell
# Discover existing clients, generate shortcuts, and start the switcher
.\.venv\Scripts\python.exe script.py

# Launch two ordinary clients, then generate and start the switcher
.\.venv\Scripts\python.exe script.py 2

# Launch two ordinary clients only
.\.venv\Scripts\python.exe clientLauncher.py 2

# Discover clients only
.\.venv\Scripts\python.exe pidCrawler.py

# Generate the AHK script from the saved PID list
.\.venv\Scripts\python.exe fileWriter.py

# Start the existing AHK script without rediscovery
.\.venv\Scripts\python.exe script.py --start-ahk
```

## Custom installation paths

The ordinary client launcher defaults to this legacy executable:

```text
C:\Program Files\Jagex\RuneScape Launcher\RuneScape.exe
```

If that executable is unavailable, open clients through your normal launcher and
use the existing-client workflow. To configure another directly launchable
executable:

```powershell
$env:RS3_CLIENT_PATH = 'D:\Games\RuneScape\RuneScape.exe'
.\.venv\Scripts\python.exe clientLauncher.py 2
```

AutoHotkey discovery checks per-user and system registry installation paths,
standard per-user and Program Files folders, and v2 executable names on PATH.
To override discovery, point to an AutoHotkey **v2 interpreter**, for example:

```powershell
$env:AUTOHOTKEY_PATH = "$env:LOCALAPPDATA\Programs\AutoHotkey\v2\AutoHotkey64.exe"
.\.venv\Scripts\python.exe script.py --start-ahk
```

For the batch menu, a custom Python interpreter can also be selected:

```powershell
$env:PYTHON_EXE = 'D:\Python\python.exe'
.\execute.bat
```

Install `requirements.txt` using whichever Python interpreter you select.
These PowerShell environment settings apply to the current shell and programs
started from it. Start the batch menu from that shell to use them.

## Troubleshooting

| Problem | What to do |
| --- | --- |
| `Python was not found` or the Microsoft Store opens | Use the full installed Python path to create `.venv`, then use `.venv\Scripts\python.exe`. The batch menu can find standard installations without PATH. |
| `No module named psutil` | Run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, or install with the custom interpreter selected for the menu. |
| AutoHotkey executable not found | Install v2, or set `AUTOHOTKEY_PATH` to its interpreter as shown above. |
| AHK syntax error about v1/v2 | Run the generated file using AutoHotkey v2. Regenerate it if it came from an older version of this project. |
| No clients found | Open the actual game windows first. Run discovery outside Sandboxie on the same desktop and Windows user session. |
| A shortcut does nothing | Regenerate the PID list and AHK script, then restart it. Confirm the target client is still running. |
| Elevated clients cannot be focused | Try running clients and the switcher with matching privilege levels. |
| Client executable not found | Configure `RS3_CLIENT_PATH`, or launch through Jagex/Sandboxie manually and use the existing-client workflow. |
| More than 36 clients found | Close extra clients before generating the script; generation supports at most 36 unique PIDs. |

`pidlist.txt` and `GeneratedWindowsSwitcher.ahk` are generated locally and ignored
by Git. They are created beside the Python files, regardless of the working
folder used to run the scripts. You do not need to create them during setup.

## Usage notice

The generated shortcuts only focus windows; they do not send gameplay inputs.
I shared this project with Jagex moderators without receiving
an endorsement. The historical discussion is available in the
[original Reddit thread](https://www.reddit.com/r/runescape/comments/rtzax9/can_a_jmod_please_confirm_if_this_tool_doesnt/).
Use at your own risk.

## Original video demo

[![RuneScape multiclient window-switcher demo](https://img.youtube.com/vi/k8eRO7Cnh6g/0.jpg)](https://www.youtube.com/watch?v=k8eRO7Cnh6g)

The video demonstrates the original version; follow the instructions above for
the current Python and AutoHotkey v2 setup.

## Author and attribution

Created by [Guan Hao Wu](https://github.com/guanhaowu).

I wrote this tool except for the original PID crawler, which was adapted from
externally sourced code. The PID crawler has since been updated to support
Sandboxie client discovery.
