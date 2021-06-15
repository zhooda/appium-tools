import subprocess
import sys

from downgrade_chrome import get_devices

PORT = 4723
SYS_PORT = 8200

def create_server_command(port: int, system_port: int):
    cmd = (f"appium --allow-insecure chrome_autodownload "
           f"-p {port} -dc {{\"systemPort\":{system_port}}}")
    return cmd.split()

if __name__ == "__main__":
    if not get_devices():
        sys.exit(0)
    try:
        childprocs = []
        for i in range(get_devices()):
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
        