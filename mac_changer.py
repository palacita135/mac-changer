# Author: Dirty Heroes 😈

import os
import random
import re
import subprocess
import time

# Define your network interface (change based on your system)
INTERFACE = "wlan0"  # Change to "wlan0" for WiFi or "eth0" for Ethernet

def get_current_mac(interface):
    """Get the current MAC address of the interface."""
    try:
        output = subprocess.check_output(f"ifconfig {interface}", shell=True).decode()
        mac_address = re.search(r"(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)", output).group(0)
        return mac_address
    except Exception:
        return None

def random_mac():
    """Generate a random MAC address."""
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

def change_mac(interface):
    """Change the MAC address of the specified interface."""
    old_mac = get_current_mac(interface)
    new_mac = random_mac()

    print(f"[*] Current MAC: {old_mac}")
    print(f"[*] Changing MAC to: {new_mac}")

    os.system(f"sudo ifconfig {interface} down")
    os.system(f"sudo macchanger -m {new_mac} {interface}")
    os.system(f"sudo ifconfig {interface} up")

    new_mac_confirmed = get_current_mac(interface)
    
    if new_mac == new_mac_confirmed:
        print(f"[✔] MAC Successfully Changed to {new_mac_confirmed}")
    else:
        print("[!] MAC Change Failed!")

def auto_mac_changer(interval=60):
    """Automatically change MAC address every X seconds."""
    while True:
        change_mac(INTERFACE)
        print(f"[*] Waiting {interval} seconds before next change...\n")
        time.sleep(interval)

if __name__ == "__main__":
    auto_mac_changer(interval=60)  # Change MAC every 60 seconds
