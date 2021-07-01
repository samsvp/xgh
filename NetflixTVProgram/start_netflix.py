# code to connect to mobile netflix
# %%
import subprocess
import xml.etree.ElementTree as ET
from time import sleep
from typing import List


def get_app_xml(filename: str):
    pull_xml = "adb shell uiautomator dump"
    output = subprocess.check_output(pull_xml.split(" "))
    out_file = str(output).split(" ")[-1].replace("\\r", "").replace("\\n", "").replace("'", "")

    pull_file = f"adb pull {out_file} {filename}"
    subprocess.run(pull_file.split(" "))

def get_bounds(filename: str, att: str, value: str, index: int) -> List[int]:
    root = ET.parse(filename).getroot()
    str_bounds = list(filter(
        lambda x: value in x.get(att), root.findall(f".//node[@{att}]"))
    )[index].attrib["bounds"]
    bounds = [int(s) for s in str_bounds.replace("[", "").replace("]",",").split(",") if s.isdigit()]
    return bounds

def tap(bounds: List[int]):
    x = (bounds[0] + bounds[2]) // 2
    y = (bounds[1] + bounds[3]) // 2
    tap = f"adb shell input tap {x} {y}"
    subprocess.run(tap.split(" "))

# %%
# open netflix mobile
open_command = "adb shell monkey -p com.netflix.mediaclient -c android.intent.category.LAUNCHER 1"
subprocess.run(open_command.split(" "))
# %%
# login screen
home_file = "app_home.xml"
get_app_xml(home_file)

bounds = get_bounds(home_file, "clickable", "true", 0)
tap(bounds)
# %%
# config screen
config_file = "app_home.xml"
get_app_xml(config_file)

bounds = get_bounds(config_file, "clickable", "true", 1)
tap(bounds)
# %%
