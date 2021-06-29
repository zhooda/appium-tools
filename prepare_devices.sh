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

# deactivate env
deactivate
