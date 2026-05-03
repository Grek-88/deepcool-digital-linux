import time
import psutil
import os

def find_device():
    # Search for DeepCool device (Vendor ID: 3633)
    for i in range(16):
        path = f'/dev/hidraw{i}'
        if os.path.exists(path):
            try:
                with open(f'/sys/class/hidraw/hidraw{i}/device/uevent', 'r') as f:
                    if "3633" in f.read():
                        return path
            except:
                continue
    return None

def get_stats():
    try:
        temps = psutil.sensors_temperatures()
        # Using k10temp for AMD CPU temperature
        cpu_temp = int(temps['k10temp'][0].current) if 'k10temp' in temps else 0
        cpu_load = int(psutil.cpu_percent(interval=None))
        return cpu_temp, cpu_load
    except:
        return 0, 0

def send_temp(dev, val):
    pkt = bytearray(64)
    pkt[0], pkt[1] = 0x13, max(1, min(10, int((val - 40) / 5) + 1))
    pkt[3], pkt[4] = val // 10, val % 10
    dev.write(pkt); dev.flush()

def send_load(dev, val):
    pkt = bytearray(64)
    pkt[0], pkt[1] = 0x4C, max(1, min(10, int(val / 10)))
    pkt[3], pkt[4] = val // 10, val % 10
    dev.write(pkt); dev.flush()

print("--- DeepCool Monitor: Auto-Detection Mode ---")
psutil.cpu_percent(interval=None)

while True:
    device_path = find_device()
    if not device_path:
        print("Device not found! Waiting 10s...", end='\r')
        time.sleep(10)
        continue

    print(f"Found device at: {device_path}")
    try:
        with open(device_path, 'wb') as dev:
            while True:
                # Temperature display cycle
                for _ in range(15):
                    t, l = get_stats()
                    send_temp(dev, t)
                    print(f"DISPLAY: TEMP {t}°C | CPU {l}%    ", end='\r')
                    time.sleep(1)
                # Load display cycle
                for _ in range(15):
                    t, l = get_stats()
                    send_load(dev, l)
                    print(f"DISPLAY: LOAD {l}% | TEMP {t}°C    ", end='\r')
                    time.sleep(1)
    except Exception as e:
        print(f"\nConnection lost ({e}). Re-scanning...")
        time.sleep(2)
