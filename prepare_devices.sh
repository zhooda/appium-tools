#!/bin/bash

# activate venv
cd /Users/pankajakshanramaswamy/Repositories/appium-tools
source ./venv/bin/activate

# fix_devices.py
python fix_devices.py

# uninstall.py
python uninstall.py

# deactivate env
deactivate
