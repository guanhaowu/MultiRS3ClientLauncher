# MultiRS3ClientLauncher

This is a simple script for Windows to start up X amount of client and generate a keybind to each window so you can swap between them by pressing the keybind.
The max clients is 36.

## Warning
**PLEASE USE AT YOUR OWN RISK** 
This is basically a sort of MACRO to keybind your RS client to a key. 
It only does **1:1 action**, which should be allowed according to Jagex ToS.

PS: I've sent this github page to Jmods before on twitch, but they've never commented on it, so please use this at your own risk.
I've made a post on reddit about this, an user linked me to another post of 5years ago where JmodTyra stated that AHK not allowed, but another player quoted another statement (source still needs to be confirmed) "Unless it is used to remap a key to any other button". [Read Reddit thread here](https://www.reddit.com/r/runescape/comments/rtzax9/can_a_jmod_please_confirm_if_this_tool_doesnt/).

## Video demo:
[![IMAGE ALT TEXT](http://img.youtube.com/vi/k8eRO7Cnh6g/0.jpg)](http://www.youtube.com/watch?v=k8eRO7Cnh6g "RuneScape Simple Multiclient tool demo")


## Requirement
* Windows machine
* [Python version 3.7](https://www.python.org/downloads/) installed and set in system PATH
* [AutoHotkey](https://www.autohotkey.com/) installed

### Machine Support
* Tested on Windows 10 version 1909.

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
