import os
import time
import json
import threading
import subprocess
from collections import deque
from datetime import datetime

import utils

from typing import Dict, List


class Device(threading.Thread):

    num_threads = 0
 
    app_to_json = {
        "Amazon": "channels/amazon_channels.json",
        "Globo": "channels/globo_channels.json",
        "Netflix": "channels/netflix_channels.json",
    }

    app_names = {
        "Amazon": "amazon.avod",
        "Globo": "globo",
        "Netflix": "netflix",
        "Youtube": "youtube"
    }


    def __init__(self, IP: str, app: str, internet: bool) -> None:
        threading.Thread.__init__(self)
        Device.num_threads += 1

        # thread variables
        self.threadID = Device.num_threads
        self.name = f"Thread{self.threadID}"
        self.counter = self.threadID
        self._running = False

        # device info
        self.IP = IP
        self.app = app
        self.internet = internet # use internet check

        # time passed since streaming started
        self.time_passed = 0

        # metadata
        self.channel = ""
        self.log_max_length = 100 # max amount of text to log
        self.log = deque([])


    def run(self) -> None:
        self._update_log(f"Starting thread {self.threadID}")

        self.connect()

        self._running = True
        while self._running:
            self.update()

        self._update_log(f"Thread {self.threadID} killed")


    def terminate(self):
        """
        Kills thread
        """
        self._running = False


    def update(self) -> None:
        channels = self.read_channels()
        for channel, channel_info in channels.items():
            self._update_log(f"current program: {channel}")
            
            self.channel = channel
            self.url = channel_info["url"]
            duration = utils.time_to_seconds(channel_info["duration"])

            self.go_to_current_url()
            self.wait_to_finish(duration, duration_offset=2)


    def connect(self) -> None:
        while not self.is_connected():
            # disconnect if adb marks device as offline
            os.system(f"adb disconnect {self.IP}")
            os.system(f"adb connect {self.IP}")

        self._update_log(f"Connected to device {self.IP}")


    def is_connected(self) -> bool:
        """
        Returns whether or not the device is connected via adb
        """
        connected_IPs = utils.get_connected_devices()
        return self.IP in connected_IPs


    def go_to_current_url(self) -> None:
        os.system(f"adb -s {self.IP} shell am start -a android.intent.action.VIEW -d {self.url}")


    def check_internet(self, tries=3) -> bool:
        """
        Checks if the device is connected to the internet
        """
        digits = len(str(tries))

        # ping google to check internet
        try:
            output = str(subprocess.check_output(f"adb -s {self.IP} shell ping -c {tries} google.com"))
            received_text = next(line for line in output.split("\n") if "received" in line)
        except (subprocess.CalledProcessError, StopIteration):
            return False

        # get the index of the start of the packages received info
        index = received_text.find(" received")
        # packages received
        packages = int(received_text[index-digits: index])

        return packages > 0


    def get_current_app(self) -> str:
        """
        Returns the current open app or its info
        """
        try:
            output = str(subprocess.check_output(f"adb -s {self.IP} shell dumpsys window windows")).split("\\r\\n")
            focused_app_info = next(line for line in output if "mFocusedApp"in line)
            if Device.app_names[self.app] in focused_app_info:
                return self.app
            else:
                return focused_app_info
        except (subprocess.CalledProcessError, StopIteration):
            return ""


    def read_channels(self) -> Dict[str, Dict[str, str]]:
        with open(Device.app_to_json[self.app]) as f:
            channels = json.load(f)

        return channels


    def _update_log(self, message: str) -> None:
        """
        Adds the current message to the log
        """
        print(message)
        self.log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
        if len(self.log) > self.log_max_length: self.log.popleft()


    def get_log(self) -> List[str]:
        return self.log


    def wait_to_finish(self, duration: int, duration_offset=2) -> None:
        """
        Counts down to wait for the current movie/series to finish.
        params:
        duration: duration of the movie in seconds
        internet: check for internet connection access
        duration_offset: amount in seconds to be added to the movie duration
        """
        while self.time_passed < duration + duration_offset:
            loop_begin = time.time()
            time.sleep(1)

            # device disconnected
            if not self.is_connected():
                self._update_log("Device has been disconnected from adb")
                self.connect()
                self.go_to_current_url()
            # app closed, so open it again
            elif self.app != self.get_current_app():
                self._update_log(f"Current app changed. Returning to {self.app}.")
                self.go_to_current_url()
            # we don't have internet, stop counting down
            elif self.internet and not self.check_internet(): 
                self._update_log("Internet disconnected")
            # everything is fine, increment timer
            else: 
                self.time_passed += time.time() - loop_begin
        
        self.time_passed = 0
