import downgrade_chrome as dg

if __name__ == '__main__':
    devices = dg.CLIENT.devices()

    for device in devices:
        model = device.shell("getprop ro.product.model").strip()
        udid = device.shell("getprop ro.serialno").strip()
        print(model, ":", dg.get_app_version(device, "com.google.android.webview"), ":", udid)

