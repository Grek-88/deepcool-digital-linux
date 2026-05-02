# DeepCool AK400 Digital SE Display Driver (Linux - tested on Mint)

Python script and systemd service to drive DeepCool Digital status displays on Linux.

## Features
- Switches between **CPU Temperature** and **CPU Usage** every 15 seconds.
- Dynamic progress bar logic (40-90°C for temp, 0-100% for load).
- Runs as a background service.

## Installation

1. **Check your Device ID:**
   Run `lsusb` in your terminal. Look for a line like this:
   `Bus 001 Device 004: ID 3633:0001 DeepCool A400-DIGITAL`

2. **Clone and Install:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/deepcool-digital-linux
   cd deepcool-digital-linux
   chmod +x install.sh
   ./install.sh
   ```

> **Note:** If your ID is NOT `3633:0001`, open `install.sh` and edit the `idVendor` and `idProduct` values before running the installer.

## Management
- **Stop:** `sudo systemctl stop deepcool`
- **Start:** `sudo systemctl start deepcool`
- **Status:** `sudo systemctl status deepcool`
- **Logs:** `journalctl -u deepcool -f`
