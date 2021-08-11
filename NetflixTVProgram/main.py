# %%
import device

devs = { "192.168.0.148": {"app": "Netflix", "internet": True} }

# %%
if __name__ == '__main__':
    devices = {IP: device.Device(IP, devs[IP]["app"], devs[IP]["internet"]) for IP in devs}
    for IP, dev in devices.items():
        print(f"starting device with IP {IP}")
        dev.start()
        # dev.run()
# %%
