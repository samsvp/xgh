#%%
import subprocess

def check_internet(tries=3) -> bool:
    digits = len(str(tries))

    # ping google to check internet
    output = str(subprocess.check_output(f"adb shell ping -c {tries} google.com"))
    received_text = next(line for line in output.split("\n") if "received" in line)

    # get the index of the start of the packages received info
    index = received_text.find(" received")
    # packages received
    packages = int(received_text[index-digits: index])

    return packages > 0
# %%
