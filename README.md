# MultiRS3ClientLauncher

This is a simple script for Windows to start up X amount of client and generate a keybind to each window so you can swap betweem them by pressing the keybind.
The max clients is 36.

## Warning
**PLEASE USE AT YOUR OWN RISK**

## Requirement
* [Python version 3.7](https://www.python.org/downloads/) installed and set in system PATH
* [AutoHotkey](https://www.autohotkey.com/) installed 

## Usage
 1. Download the whole folder and keep the files in the same folder.
 2. Run the **execute.bat** file
 3. Choose an option.
 
### Options
```batch
Echo Choose an option:
Echo 1: Start everything.
Echo 2: Launch RS3 Clients.
Echo 3: Generate PID File.
Echo 4: Create AHK script.
Echo 5: Start AHK script.
Echo 6: Exit.
```
 
## Keybinds
* The first 12 clients (1-12) will be set to: **`F1`** - **`F12`**
* The next 12 clients (13-24) will be set to: **`SHIFT`+`F1`** - **`SHIFT`+`F12`**
* The last 12 clients (25-36) will be set to: **`CTRL`+`SHIFT`+`F1`** - **`CTRL`+`SHIFT`+`F12`**

Made by [Guan Hao Wu](https://github.com/guanhaowu) just for fun.
