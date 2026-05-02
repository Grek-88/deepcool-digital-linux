#!/bin/bash

echo "--- DeepCool Digital Linux Installer ---"

# 1. Install dependencies
sudo apt update && sudo apt install -y python3-psutil

# 2. Setup udev rules (access without sudo)
echo 'KERNEL=="hidraw*", ATTRS{idVendor}=="3633", ATTRS{idProduct}=="0001", MODE="0666"' | sudo tee /etc/udev/rules.d/99-deepcool.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

# 3. Create systemd service
SCRIPT_PATH=$(pwd)/main.py

cat <<SERVICE | sudo tee /etc/systemd/system/deepcool.service
[Unit]
Description=DeepCool Digital Display Monitor
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
SERVICE

# 4. Enable and Start
sudo systemctl daemon-reload
sudo systemctl enable deepcool.service
sudo systemctl start deepcool.service

echo "------------------------------------------------"
echo "Done! Display should be active."
echo "Manage with: sudo systemctl stop/start deepcool"
