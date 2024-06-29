from simple import MQTTClient
import config
import machine
from ubinascii import hexlify

# Adafruit IO MQTT setup
AIO_SERVER = 'io.adafruit.com'
AIO_PORT = 1883
AIO_USERNAME = config.AIO_USERNAME
AIO_KEY = config.AIO_KEY

# Feeds
AIO_FEED_TEMPERATURE = AIO_USERNAME + '/feeds/temperature'
AIO_FEED_HUMIDITY = AIO_USERNAME + '/feeds/humidity'
AIO_FEED_CONTROLLER = AIO_USERNAME + '/feeds/controller'

def connect():
    client = MQTTClient(client_id=hexlify(machine.unique_id()),
                        server=AIO_SERVER,
                        port=AIO_PORT,
                        user=AIO_USERNAME,
                        password=AIO_KEY,
                        keepalive=60)
    client.connect()
    print("Connected to Adafruit IO MQTT Broker")
    return client

def send_data(client, feed, value):
    try:
        topic = bytes(feed, 'utf-8')
        msg = bytes(str(value), 'utf-8')
        client.publish(topic, msg)
        print("Sent data to feed:", feed, "Value:", value)
    except Exception as e:
        print("Failed to send data to feed:", feed, "Error:", e)
