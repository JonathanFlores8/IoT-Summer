from machine import Pin
from utime import sleep
from dht import DHT11
import network_manager
import mqtt_manager

# Ensure Wi-Fi is connected
if not network_manager.wlan.isconnected():
    print("Wi-Fi connection failed. Exiting...")
    exit()

# Connect to Adafruit IO MQTT broker
mqtt_client = mqtt_manager.connect()

# Pin setup for DHT11 sensor
sensor = DHT11(Pin(16))

# Pin setup for LED
led_pin = Pin("LED", Pin.OUT)

# Variable to store LED state
led_state = False

# Callback for MQTT messages
def message_callback(topic, msg):
    global led_state
    if topic == bytes(mqtt_manager.AIO_FEED_CONTROLLER, 'utf-8'):
        if msg == b"ON":
            led_state = True
        elif msg == b"OFF":
            led_state = False
        led_pin.value(led_state)
        print("Received message: {} - LED state: {}".format(msg.decode(), "ON" if led_state else "OFF"))

# Set the callback function
mqtt_client.set_callback(message_callback)

# Subscribe to the feed
mqtt_client.subscribe(mqtt_manager.AIO_FEED_CONTROLLER)

try:
    while True:
        try:
            # Read data from DHT11
            sensor.measure()
            temperature = sensor.temperature()
            humidity = sensor.humidity()
            
            # Print sensor data
            print('Temperature: {}°C Humidity: {}%'.format(temperature, humidity))
            
            # Send data to Adafruit IO
            mqtt_manager.send_data(mqtt_client, mqtt_manager.AIO_FEED_TEMPERATURE, temperature)
            mqtt_manager.send_data(mqtt_client, mqtt_manager.AIO_FEED_HUMIDITY, humidity)
            
            # Check for new messages
            mqtt_client.check_msg()
            
            sleep(5)
        except Exception as e:
            print("Failed to read from sensor or send data:", e)
            sleep(5)
except KeyboardInterrupt:
    print("Script interrupted by user. Disconnecting...")
finally:
    mqtt_client.disconnect()
    print("Disconnected from Adafruit IO MQTT Broker. Exiting...")
