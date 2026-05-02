import time
import psutil
import os

# --- Configuration ---
DEV_PATH = '/dev/hidraw4'
TEMP_MIN = 40
TEMP_MAX = 90
CYCLE_SECONDS = 15

def get_stats():
    try:
        temps = psutil.sensors_temperatures()
        cpu_temp = 0
        if 'k10temp' in temps:
            cpu_temp = int(temps['k10temp'][0].current)
        # Non-blocking call to get CPU load
        cpu_load = int(psutil.cpu_percent(interval=None))
        return cpu_temp, cpu_load
    except:
        return 0, 0

def temp_to_bar(val):
    if val <= TEMP_MIN:
        return 1
    elif val >= TEMP_MAX:
        return 10
    else:
        return int((val - TEMP_MIN) / ((TEMP_MAX - TEMP_MIN) / 10)) + 1

def load_to_bar(val):
    if val == 0:
        return 0
    return max(1, min(10, int(val / 10)))

def send_temp(dev, val):
    pkt = bytearray(64)
    pkt[0] = 0x13
    pkt[1] = temp_to_bar(val)
    pkt[2] = 0x00
    pkt[3] = val // 10
    pkt[4] = val % 10
    try:
        dev.write(pkt)
        dev.flush()
    except:
        pass

def send_load(dev, val):
    pkt = bytearray(64)
    pkt[0] = 0x4C
    pkt[1] = load_to_bar(val)
    pkt[2] = 0x00
    pkt[3] = val // 10
    pkt[4] = val % 10
    try:
        dev.write(pkt)
        dev.flush()
    except:
        pass

print("--- DeepCool Monitor Started ---")
print(f"Modes: {CYCLE_SECONDS}s Temperature / {CYCLE_SECONDS}s Load")
print("Press Ctrl+C to stop\n")

# Warm up psutil — first call always returns 0
psutil.cpu_percent(interval=None)

while True:
    try:
        if not os.path.exists(DEV_PATH):
            raise Exception(f"Device {DEV_PATH} not found")

        dev = open(DEV_PATH, 'wb')

        # TEMPERATURE Cycle
        for _ in range(CYCLE_SECONDS):
            t, l = get_stats()
            send_temp(dev, t)
            print(f"DISPLAY: TEMP {t}°C | CPU: {l}%    ", end='\r')
            time.sleep(1)

        # LOAD Cycle
        for _ in range(CYCLE_SECONDS):
            t, l = get_stats()
            send_load(dev, l)
            print(f"DISPLAY: LOAD {l}%  | TEMP: {t}°C    ", end='\r')
            time.sleep(1)

        dev.close()

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
        try:
            dev.close()
        except:
            pass
        break
    except Exception as e:
        print(f"\nError: {e} — restarting in 5 sec...")
        time.sleep(5)
