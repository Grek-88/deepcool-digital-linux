#!/bin/bash
echo "--- DeepCool Digital Linux Installer ---"

# 1. Зависимости
sudo apt update && sudo apt install -y python3-psutil

# 2. Права USB
echo 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="3633", ATTRS{idProduct}=="0001", MODE="0666", GROUP="plugdev"' | sudo tee /etc/udev/rules.d/99-deepcool.rules
sudo udevadm control --reload-rules && sudo udevadm trigger

# 3. Служба
SCRIPT_PATH=$(pwd)/main.py
cat <<SERVICE | sudo tee /etc/systemd/system/deepcool.service
[Unit]
Description=DeepCool Digital Display Monitor
After=multi-user.target

[Service]
Type=simple
ExecStartPre=/bin/sleep 10
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=always
User=$USER
WorkingDirectory=$(pwd)

[Install]
WantedBy=multi-user.target
SERVICE

# 4. Запуск
sudo systemctl daemon-reload
sudo systemctl enable deepcool.service
sudo systemctl restart deepcool.service

echo "Done!"
