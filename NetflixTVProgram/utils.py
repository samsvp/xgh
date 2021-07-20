import subprocess

from typing import Dict, List


app_to_json = {
    "Netflix": "channels.json",
    "Amazon": "amazon_channels.json",
}

def get_connected_devices() -> List[str]:
    """
    Returns connected devices
    """
    devices_command = "adb devices"
    output = subprocess.check_output(devices_command.split(" "))
    on = [line.split(b":")[0].decode("utf-8") for line in output.splitlines() 
            if b"device" in line and b"offline" not in line]
    return on


def time_to_seconds(mtime) -> int:
    hours, minutes, seconds = [int(t) for t in mtime.split(":")]
    return hours * 60 ** 2 + minutes * 60 + seconds