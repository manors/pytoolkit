#!/usr/bin/env python3
#charset=utf-8
"""
smart_killer
~~~~~~~~~~~~
This module will smartly kill currently activity.

The default hotkey is Ctrl+Alt+X (must be pressed twice), When it trigged the
behavior depends on the currently active application, if it is chrome / vscode,
send Ctrl + W.  Unrecognized applications will send Alt + F4 by default.

Notes:
The script will use pip to automatically install the requirements.

:copyright: (c) 2020 by manors@live.cn.
"""

import re
import time
import importlib
import importlib.util
from datetime import datetime


def require(requirements):
    """if not exists use pip install package."""
    for package, module in requirements.items():
        if not importlib.util.find_spec(module):
            import pip
            pip.main(['install', package])


require({
    'keyboard': 'keyboard',
    'pywin32': 'win32',
})

import keyboard
from win32 import win32gui
from win32 import win32api
from win32 import win32process
from win32.lib import win32con


class SmartKiller:
    """SmartKiller class"""
    def __init__(self):
        self.last_time = datetime.now()
        self.keys = []

        self.actions = [
            {
                'window': r'.+- Visual Studio Code$',
                'process': r'.+Microsoft VS Code\\Code\.exe',
                'send': 'ctrl+w',
            },
            {
                'window': r'.+- Google Chrome$',
                'process': r'.+\\chrome\.exe',
                'send': 'ctrl+w',
            },
            {
                'window': r'.+',
                'process': r'.+\\(powershell|cmd|bash|debian|ubuntu)\.exe',
                'write': '\nexit\n',
            },
            {
                'window': r'.*',
                'process': r'.*',
                'send': 'alt+f4',
            },
        ]

    def kill(self):
        """Get currently active application, send key as defined."""
        hwnd = win32gui.GetForegroundWindow()
        window_name = win32gui.GetWindowText(hwnd)
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        handle = win32api.OpenProcess(
            win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
            win32con.FALSE, pid
        )
        process_name = win32process.GetModuleFileNameEx(handle, win32con.NULL)
        print(f'window: {window_name}\nprocess: {process_name}')

        for action in self.actions:
            if re.match(action['window'], window_name) \
            and re.match(action['process'], process_name):
                print(f'matched: {action["window"]} & {action["process"]}')
                if 'send' in action.keys():
                    keyboard.send(action['send'])
                    print(f'send:{repr(action["send"])}')
                if 'write' in action.keys():
                    keyboard.write(action['write'])
                    print(f'write:{repr(action["write"])}')
                break

    def handle_hook(self, args):
        """Handle hook callback, wait for hotkey."""
        # print(args)
        if args.name in ('ctrl', 'alt', 'left ctrl', 'left alt'):
            if args.event_type == 'down':
                if args.name not in self.keys:
                    self.keys.append(args.name)
            elif args.event_type == 'up':
                if args.name in self.keys:
                    self.keys.remove(args.name)

        if args.name == 'x' and args.event_type == 'down':
            if ('ctrl' in self.keys or 'left ctrl' in self.keys
               ) and ('alt' in self.keys or 'left alt' in self.keys):

                interval = (datetime.now() - self.last_time).total_seconds()
                if interval > 0.5:
                    print(f'require double click in 0.5s, current {interval}')
                    self.last_time = datetime.now()
                else:
                    print('trigged')
                    # release keys
                    for key in self.keys:
                        keyboard.release(key)
                    self.keys.clear()
                    # wait release key worked
                    time.sleep(0.02)
                    # kill
                    self.kill()

    def main(self):
        """Entry point"""
        keyboard.hook(self.handle_hook)
        keyboard.wait()


if __name__ == '__main__':
    SmartKiller().main()
