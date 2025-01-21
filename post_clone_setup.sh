#!/bin/bash

# Check if config exists
if [ ! -f ~/.zbot_config.json ]; then
    echo "No ZBot configuration found. Running setup..."
    python3 setup_zbot.py
else
    echo "ZBot configuration found. To reconfigure, run: python3 setup_zbot.py"
fi
