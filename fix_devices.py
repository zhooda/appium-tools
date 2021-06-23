"""
adb -s UDID uninstall io.appium.uiautomator2.server
adb -s UDID uninstall io.appium.uiautomator2.server.test
adb -s UDID uninstall io.appium.unlock
adb -s UDID uninstall io.appium.setting
"""

import downgrade_chrome as dg

APPIUM_ARTIFACTS = [
    "io.appium.uiautomator.server",
    "io.appium.uiautomator.server.test",
    "io.appium.uiautomator2.server",
    "io.appium.uiautomator2.server.test",
    "io.appium.unlock",
    "io.appium.setting"
]

if __name__ == "__main__":
    devices = dg.CLIENT.devices()
    
    for device in devices:
        
        try:
            model = device.shell("getprop ro.product.model").strip()
            udid = device.shell("getprop ro.serialno").strip()
        except Exception as e:
            print(f'device error: {e}')
            continue
        
        for package in APPIUM_ARTIFACTS:
            try:
                device.uninstall(package)
                print(f'{model} ({udid}) uninstalled {package}')
            except Exception as e:
                print(f'{model} ({udid}) could not uninstall {package}: {e}')