#!/bin/bash

# activate venv
# cd /Users/pankajakshanramaswamy/Repositories/appium-tools
source ./venv/bin/activate

# clean up chrome://inspect windows
osascript cleanup_chrome.applescript

# fix_devices.py
python fix_devices.py

# reboot devices
adb -s 19347523600322 reboot
adb -s 5200a594c0ba5559 reboot

sleep 5m

# uninstall.py
python uninstall.py

# deactivate env
deactivate
