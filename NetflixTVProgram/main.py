import os
import time
import json

from typing import Dict


app = "Amazon"

app_to_json = {
    "Netflix": "channels.json",
    "Amazon": "amazon_channels.json",
}

def read_channels() -> Dict[str, Dict[str, str]]:
    with open(app_to_json[app]) as f:
        channels = json.load(f)

    return channels


def time_to_seconds(mtime) -> int:
    hours, minutes, seconds = [int(t) for t in mtime.split(":")]
    return hours * 60 ** 2 + minutes * 60 + seconds


def main() -> None:
    channels = read_channels()
    while True:
        for channel, channel_info in channels.items():
            url = channel_info["url"]
            duration = time_to_seconds(channel_info["duration"])

            os.system(f"adb shell am start -a android.intent.action.VIEW -d {url}")
            time.sleep(duration + 2)
            
        break


if __name__ == '__main__':
    main()