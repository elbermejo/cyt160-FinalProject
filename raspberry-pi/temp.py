# temp.py - Send temperature data to MQTT in JSON format

import paho.mqtt.client as mqtt
import time
import json

# MQTT Settings
MQTT_BROKER = "54.196.150.30"   # your EC2 public IP
MQTT_PORT = 1883
MQTT_TOPIC = "iot/temperature"

# Path to the working sensor
device_file = '/sys/bus/w1/devices/28-00000083d804/w1_slave'  # update if your sensor ID is different

def read_temp_raw():
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

# Setup MQTT client and connect
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)


# Send temperature data every 5 seconds
while True:
    temp_c, temp_f = read_temp()
    payload = json.dumps({
        "temp_c": round(temp_c, 2),
        "temp_f": round(temp_f, 2)
    })
    print(f"Publishing: {payload}")
    client.publish(MQTT_TOPIC, payload)

    time.sleep(5)
