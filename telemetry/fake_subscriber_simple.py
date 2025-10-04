#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import random
import os
import sys

print("🚀 Starting SIMPLE fake subscriber...")

# Force flush output
sys.stdout.flush()

MQTT_BROKER = os.getenv("EMQX_HOST", "mosquitto-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))

print(f"Target: {MQTT_BROKER}:{MQTT_PORT}")

def on_connect(client, userdata, flags, rc):
    print(f"CONNECTED with code: {rc}")
    sys.stdout.flush()
    client.subscribe("devices/#")
    print("SUBSCRIBED to devices/#")
    sys.stdout.flush()

def on_message(client, userdata, msg):
    print(f"RECEIVED: {msg.topic} = {msg.payload.decode()}")
    sys.stdout.flush()

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"SUBSCRIBE confirmed for MID: {mid}")
    sys.stdout.flush()

client = mqtt.Client(client_id=f"simple-sub-{random.randint(1000,9999)}")
client.on_connect = on_connect
client.on_message = on_message

print("Connecting...")
sys.stdout.flush()

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    print("Connection call completed, starting loop...")
    sys.stdout.flush()
    
    client.loop_start()
    print("Loop started, waiting for messages...")
    sys.stdout.flush()
    
    # Keep alive with periodic messages
    counter = 0
    while True:
        time.sleep(5)
        counter += 1
        if counter % 12 == 0:  # Every minute
            print(f"💓 Still alive... ({counter//12} minutes)")
            sys.stdout.flush()
        
except Exception as e:
    print(f"ERROR: {e}")
    sys.stdout.flush()
    import traceback
    traceback.print_exc()
