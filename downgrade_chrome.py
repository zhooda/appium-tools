import logging

from ppadb.client import Client as ADBClient
from ppadb.device import Device

CLIENT = ADBClient(host="127.0.0.1", port=5037)

LOCAL_APK_PATH = "chrome_v87.0.apk"
DEVICE_APK_PATH = "/data/local/tmp/sa_automation/chrome_v87.0.apk"
CHROME_BUNDLE = "com.android.chrome"

class DowngradeError(Exception):
    """Raised when ADB app downgrade failed"""
    pass

def get_device(udid: str) -> Device:
    """Returns device with UDID"""
    return CLIENT.device(udid)

def get_app_version(device: Device, bundle: str) -> str:
    """Returns major app version from Android device"""
    
    logging.info(f'getting {bundle} version')
    
    cmd = f"dumpsys package {bundle} | grep versionName"
    versions = device.shell(cmd).strip().split('\n')#.split("=")[-1]#.split('.')[0]
    versions = [v.split('=')[-1] for v in versions]

    return min(versions)

def install_app(device: Device):
    model = device.shell("getprop ro.product.model").strip()
    logging.info(f'processing device: {model}')

    version = int(get_app_version(device, CHROME_BUNDLE).split('.')[0])

    if version >= 87:
        logging.info(f'bad {CHROME_BUNDLE} version: {version}')
        
        logging.info(f'pushing {LOCAL_APK_PATH} to {DEVICE_APK_PATH}')
        device.push(LOCAL_APK_PATH, DEVICE_APK_PATH)
        
        logging.info(f'downgrading {CHROME_BUNDLE} to {DEVICE_APK_PATH}')
        output = device.shell(f"pm install -d {DEVICE_APK_PATH}").strip()
        logging.info(f'downgrade status: {output}')
        
        logging.info(f'cleaning up {CHROME_BUNDLE} remenants')
        device.shell(f"rm -f {DEVICE_APK_PATH}")
        
        if not output.startswith('Success'):
            raise DowngradeError((f"Could not downgrade {CHROME_BUNDLE}"
                                    f" to {DEVICE_APK_PATH}"))
    else:
        logging.info(f'{CHROME_BUNDLE} version {version} OK!')
        
    logging.info(f'finished processing device: {model}')

def main():
    # 127.0.0.1:5037 is the default
    logging.info('starting ADB client')
    client = ADBClient(host="127.0.0.1", port=5037)

    logging.info('getting connected devices')
    devices = client.devices()

    for device in devices:
        model = device.shell("getprop ro.product.model")
        logging.info(f'processing device: {model}')
        version = get_app_version(device, CHROME_BUNDLE)

        if version >= 87:
            logging.info(f'bad {CHROME_BUNDLE} version: {version}')
            
            logging.info(f'pushing {LOCAL_APK_PATH} to {DEVICE_APK_PATH}')
            device.push(LOCAL_APK_PATH, DEVICE_APK_PATH)
            
            logging.info(f'downgrading {CHROME_BUNDLE} to {DEVICE_APK_PATH}')
            output = device.shell(f"pm install -d {DEVICE_APK_PATH}").strip()
            logging.info(f'downgrade status: {output}')
            
            device.shell(f"rm -f {DEVICE_APK_PATH}")
            
            if not output.startswith('Success'):
                raise DowngradeError((f"Could not downgrade {CHROME_BUNDLE}"
                                      f" to {DEVICE_APK_PATH}"))
        else:
            logging.info(f'{CHROME_BUNDLE} version {version} OK!')
            
        logging.info(f'finished processing device: {model}')
            
if __name__ == "__main__":
    
    FORMAT = "[%(levelname)s] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    
    # try:
    #     main()
    # except DowngradeError as e:
    #     logging.error(f'Error downgrading chrome version: {e}. Please try again')
    
    devices = CLIENT.devices()
    
    for device in devices:
        install_app(device)