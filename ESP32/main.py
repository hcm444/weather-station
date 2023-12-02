
import network
import utime
from machine import Pin
import dht
import ujson
import ubinascii
import os
from umqtt.simple import MQTTClient

# Function to generate a unique ID
def generate_sensor_id():
    random_id = ubinascii.hexlify(os.urandom(4)).decode()
    return f"{random_id}"

# Function to get the current UTC timestamp
def get_utc_timestamp():
    return utime.time()

# MQTT Server Parameters
MQTT_CLIENT_ID = generate_sensor_id()
MQTT_BROKER = "broker.hivemq.com"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC = "solar1"

sensor = dht.DHT22(Pin(15))

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    utime.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

prev_weather = ""
while True:
    print("Measuring weather conditions... ", end="")
    sensor.measure()
    
    # Include UTC timestamp in the message
    timestamp_utc = get_utc_timestamp()
    message = ujson.dumps({
        "sensor_id": MQTT_CLIENT_ID,
        "temp": sensor.temperature(),
        "humidity": sensor.humidity(),
        "timestamp_utc": timestamp_utc
    })
    
    if message != prev_weather:
        print("Updated!")
        print("Reporting to MQTT topic {}: {}".format(MQTT_TOPIC, message))
        client.publish(MQTT_TOPIC, message)
        prev_weather = message
    else:
        print("No change")
    utime.sleep(1)
