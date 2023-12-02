from flask import Flask, render_template
import json
import paho.mqtt.client as mqtt
app = Flask(__name__)
mqtt_broker_address = "broker.hivemq.com"
mqtt_topic = "solar1"
iot_devices = {}
def on_connect(client, userdata, flags, rc):
    client.subscribe(mqtt_topic)
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))

    sensor_id = payload.get("sensor_id", "unknown")

    iot_devices[sensor_id] = payload
    print(f"Received message from {sensor_id}: {payload}")
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker_address, 1883, 60)
mqtt_client.loop_start()
@app.route("/")
def index():

    devices_list = list(iot_devices.values())
    return render_template("index.html", iot_devices=devices_list)
if __name__ == "__main__":
    app.run(debug=True)
