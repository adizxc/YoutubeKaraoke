#!/bin/bash

# Install required packages
opkg update
opkg install python3 python3-pip python3-venv

# Create application directory
mkdir -p /opt/youtube-queue

# Copy application files
cp -r * /opt/youtube-queue/

# Create virtual environment and install dependencies
cd /opt/youtube-queue
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install service
cp youtube-queue.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable youtube-queue
systemctl start youtube-queue

echo "Installation complete. The application should be running on port 5002"
