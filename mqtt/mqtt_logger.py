#!/usr/bin/env python3
import paho.mqtt.client as mqtt

LOG_FILE = "/home/group8/iot_temp.log"
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/temperature"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    print(f"Received: {message}")
    with open(LOG_FILE, "a") as f:
        f.write(message + "\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()
