#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_config_path():
    return Path.home() / ".zbot_config.json"


def save_config(config):
    with open(get_config_path(), "w") as f:
        json.dump(config, f, indent=2)


def load_config():
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def get_user_input(prompt, options=None):
    while True:
        print(prompt)
        if options:
            for i, opt in enumerate(options, 1):
                print(f"{i}. {opt}")
        response = input("> ").strip()
        if options:
            try:
                choice = int(response)
                if 1 <= choice <= len(options):
                    return options[choice - 1]
            except ValueError:
                pass
            print("Please enter a valid number.")
        else:
            return response


def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


def setup_zbot():
    clear_screen()
    print("ZBot Connection Setup")
    print("====================")

    # Load existing config if any
    config = load_config()

    # Get connection type
    connection_type = get_user_input(
        "\nHow are you connecting to ZBot?", ["USB Cable", "Wireless"]
    )

    if connection_type == "Wireless":
        input_type = get_user_input(
            "\nHow would you like to specify the ZBot?",
            ["ZBot Name (Z-number)", "Direct IP Address"],
        )

        if input_type == "ZBot Name (Z-number)":
            while True:
                zbot_name = get_user_input(
                    "\nEnter ZBot name (format: Z-{number}, e.g., Z-15):"
                ).upper()
                if zbot_name.startswith("Z-") and zbot_name[2:].isdigit():
                    config["ip"] = f"{zbot_name}.kscale.lan"
                    break
                print("Invalid format. Please use the format Z-{number}")
        else:  # Direct IP Address
            while True:
                ip_address = get_user_input("\nEnter IP address:")
                if validate_ip(ip_address):
                    config["ip"] = ip_address
                    break
                print("Invalid IP address format. Please use format: xxx.xxx.xxx.xxx")

            print("\nNOTE: If you need to find the IP address:")
            print("1. Connect via USB and SSH into 192.168.42.1")
            print("2. Run 'ifconfig' and look for the IP next to wlan0")
            print("3. Contact a KScale team member for assistance if needed")

    else:  # USB Cable
        config["ip"] = "192.168.42.1"
        print("\nSet to default USB IP (192.168.42.1)")

    # Save configuration
    save_config(config)
    print("\nConfiguration saved!")
    print(f"IP Address: {config['ip']}")
    input("\nPress Enter to continue...")


if __name__ == "__main__":
    setup_zbot()
