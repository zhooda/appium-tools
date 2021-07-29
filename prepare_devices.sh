#!/bin/bash

# activate venv
# cd /Users/pankajakshanramaswamy/Repositories/appium-tools
source ./venv/bin/activate

# clean up chrome://inspect windows
osascript cleanup_chrome.applescript

# fix_devices.py
python fix_devices.py

# uninstall.py
python uninstall.py

# reboot devices
adb -s 19347523600322 reboot
adb -s 5200a594c0ba5559 reboot
adb -s 20223522502768 reboot

sleep 5m

# deactivate env
deactivate
