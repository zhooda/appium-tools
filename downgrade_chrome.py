import logging
import os

from ppadb.client import Client as ADBClient
from ppadb.device import Device

from download_chrome import download_chrome_apk

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

def get_devices():
    return len(CLIENT.devices())

def get_app_version(device: Device, bundle: str) -> str:
    """Returns major app version from Android device"""
    
    logging.info(f'getting {bundle} version')
    
    cmd = f"dumpsys package {bundle} | grep versionName"
    versions = device.shell(cmd).strip().split('\n')#.split("=")[-1]#.split('.')[0]
    versions = [v.split('=')[-1].strip() for v in versions]

    return max(versions)

def validate_app_version(device: Device, version: str='87.0.4280.141') -> bool:
    return get_app_version(device, CHROME_BUNDLE) <= version

def install_app(device: Device):
    model = device.shell("getprop ro.product.model").strip()
    logging.info(f'processing device: {model}')

    version = int(get_app_version(device, CHROME_BUNDLE).split('.')[0])

    if version >= 87:
        logging.info(f'bad {CHROME_BUNDLE} version: {version}')
        
        logging.info(f'uninstalling {CHROME_BUNDLE} version: {version}')
        device.uninstall(CHROME_BUNDLE)

        logging.info(f'pushing {LOCAL_APK_PATH} to {DEVICE_APK_PATH}')
        device.push(LOCAL_APK_PATH, DEVICE_APK_PATH)
        
        logging.info(f'downgrading {CHROME_BUNDLE} to {DEVICE_APK_PATH}')
        output = device.shell(f"pm install -r {DEVICE_APK_PATH}").strip()
        
        logging.info(f'cleaning up {CHROME_BUNDLE} remenants')
        device.shell(f"rm -f {DEVICE_APK_PATH}")
        
        if not output.startswith('Success'):
            logging.error(f'downgrade failed: {output}')
        else:
            logging.info(f'downgrade status: {output}')
            # raise DowngradeError((f"Could not downgrade {CHROME_BUNDLE}"
            #                         f": {output.strip()}"))
    else:
        logging.info(f'{CHROME_BUNDLE} version {version} OK!')
        
    logging.info(f'finished processing device: {model}\n')
            
if __name__ == "__main__":
    
    FORMAT = "[%(levelname)s] %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.INFO)
    
    if not os.path.isfile(LOCAL_APK_PATH):
        logging.info('could not find apk file, downloading from drive\n')
        download_chrome_apk()
    
    devices = CLIENT.devices()
    
    for device in devices:
        try:
            install_app(device)
        except DowngradeError as e:
            logging.error(e)

    valid_versions = all(validate_app_version(device, CHROME_BUNDLE) for device in devices)
    logging.info(f'All devices have valid Chrome versions: {valid_versions}')