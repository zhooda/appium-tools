# appium-tools

A collection of tools to help make working with Appium a bit easier.

## Parallel testing

In order to run tests in parallel on different devices, you need to be running multiple servers. At the moment, you also need to specify the server port in your client library but in the future I'd like to have this behind a reverse proxy so you only have to specify the host name. To spin up as many servers as you have devices (connected via `adb`), you can use the `start_servers.py` script:

```bash
cd appium-tools
# pip3 if you have multiple versions of Python installed
pip install -r requirements.txt
python start_servers.py
```

## Downgrading Chrome versions

This is still not working as it should (Appium reports the Chrome version from before downgrading, but the downgrade does go through properly). To ensure all of your devices are on a Chrome version <= 87, you can use the `downgrade_chrome.py` script:

```bash
cd appium-tools
# pip3 if you have multiple versions of Python installed
pip install -r requirements.txt
python downgrade_chrome.py
```

## Closing `chrome://inspect` Stragglers

If `chrome://inspect` windows are open, devices do not show up in ADB. To get around this on macOS, I've included an applescript to close all Chrome tabs that contain the strings `inspect` or `DevTools`.

```bash
cd appium-tools
osascript cleanup_chrome.applescript
```