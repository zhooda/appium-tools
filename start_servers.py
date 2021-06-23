import subprocess
import sys

from downgrade_chrome import get_devices

PORT = 4725
SYS_PORT = 8200

def create_server_command(port: int, system_port: int):
    cmd = (f"appium --allow-insecure chromedriver_autodownload "
           f"-p {port} -dc").split()
    caps = f"{{\"systemPort\":{system_port}, \"chromedriverChromeMappingFile\": \"/Users/pankajakshanramaswamy/Desktop/appium-automation/drivers/mapping.json\"}}"
    
    caps = ( "{"
            f'"systemPort": {system_port}}}') #,'
 #           f'"chromedriverChromeMappingFile": "/Users/pankajakshanramaswamy/Desktop/appium-automation/drivers/mapping.json",'
  #          f'"chromedriverExecutableDir": "/Users/pankajakshanramaswamy/Desktop/appium-automation/drivers/"'
   #          "}")

    cmd.append(caps)
    print(' '.join(cmd))
    return cmd

if __name__ == "__main__":
    
    additional = 0
    if len(sys.argv) > 1:
        additional = int(sys.argv[-1])
    
    if not get_devices():
        sys.exit(0)
    try:
        childprocs = []
        for i in range(get_devices() + additional):
            proc = subprocess.Popen(create_server_command(PORT + i, SYS_PORT + i))
            childprocs.append(proc)
        while True: pass
    except KeyboardInterrupt:
        for proc in childprocs:
            proc.terminate()
    except Exception as e:
        print(e, file=sys.stderr)
        for proc in childprocs:
            proc.terminate()
        
