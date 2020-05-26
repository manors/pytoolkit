# pytoolkit

## smart_killer
This module will smartly kill currently activity.

### Overview
The default hotkey is Ctrl+Alt+X (must be pressed twice), When it trigged the
behavior depends on the currently active application, if it is chrome / vscode,
send Ctrl + W.  Unrecognized applications will send Alt + F4 by default.

### Usage
1. run smart_killer.pyw, no terminal or window shown
2. use hotkey, default is Ctrl+Alt+X (must be pressed twice)

### Notes
The script will use pip to automatically install the requirements.

:copyright: (c) 2020 by manors@live.cn.