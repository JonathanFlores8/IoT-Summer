import network
import time
import config

# Wi-Fi credentials from config module
SSID = config.WIFI_SSID
PASSWORD = config.WIFI_PASSWORD

# Initialize the network interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to the Wi-Fi network
print("Connecting to Wi-Fi...")
wlan.connect(SSID, PASSWORD)

# Wait for connection
max_attempts = 10
attempts = 0

while not wlan.isconnected() and attempts < max_attempts:
    print("Attempting to connect to Wi-Fi, attempt", attempts + 1)
    time.sleep(1)
    attempts += 1

if wlan.isconnected():
    print("Connected to Wi-Fi!")
    print("Network configuration:", wlan.ifconfig())
else:
    print("Failed to connect to Wi-Fi")
