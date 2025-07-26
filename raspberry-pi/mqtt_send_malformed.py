#!/usr/bin/env python3

import paho.mqtt.publish as publish
import time

BROKER = "54.196.150.30"  # <-- change to your MQTT broker IP
PORT = 1883
TOPIC = "test/topic"

# List of test payloads: some valid, some intentionally malformed
payloads = [
    '{"sensor":"temp","value":100}',                  # ✅ valid JSON
    '{"sensor":"temp","value":100',                   # ❌ missing closing brace
    '"sensor":"temp","value":100}',                   # ❌ missing opening brace
    '{"sensor":"temp","value":}',                     # ❌ missing value
    '{"sensor":"temp",}',                             # ❌ trailing comma
    '{"sensor":"temp","value":100},',                 # ❌ extra comma
    '{sensor:"temp","value":100}',                    # ❌ unquoted keys
    '{"sensor":"temp","value":"100"}',                # ✅ valid with quoted value
    '{"sensor":"temp""value":100}',                   # ❌ missing comma between keys
]

print(f"Sending {len(payloads)} test MQTT payloads...")

for i, msg in enumerate(payloads):
    print(f"[{i+1}] Publishing: {msg}")
    try:
        publish.single(TOPIC, payload=msg, hostname=BROKER, port=PORT)
        time.sleep(1)  # slight delay between messages
    except Exception as e:
        print(f"Error sending message: {e}")

print("Done.")
