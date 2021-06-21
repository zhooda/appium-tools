import downgrade_chrome as dg

if __name__ == '__main__':
    devices = dg.CLIENT.devices()
    try:
        models = [d.shell("getprop ro.product.model").strip() for d in devices]
        udids = [d.shell("getprop ro.serialno").strip() for d in devices]
    except Exception as e:
        print(e)
        
    model_spacing = max(map(len, models))
    udid_spacing = max(map(len, udids))

    print(f'{"model":{model_spacing}}  {"udid":{udid_spacing}}   {"webview":13} {"chrome":13}')

    for i in range(len(devices)):
        device = devices[i]
        try:
            model, udid = models[i], udids[i]
            #model = device.shell("getprop ro.product.model").strip()
            #udid = device.shell("getprop ro.serialno").strip()
            webview_ver = dg.get_app_version(device, "com.google.android.webview")
            chrome_ver = dg.get_app_version(device, "com.android.chrome")
            
            if len(webview_ver) >= 1:
                device.uninstall("com.google.android.webview")
            if len(chrome_ver) >= 1:
                device.uninstall("com.android.chrome")
            
            webview_ver = dg.get_app_version(device, "com.google.android.webview")[0]
            chrome_ver = dg.get_app_version(device, "com.android.chrome")[0]
            
            print(f'{model:{model_spacing}} ({udid:{udid_spacing}}): {webview_ver:13} {chrome_ver:13}')
        except Exception as e:
            print(e)

