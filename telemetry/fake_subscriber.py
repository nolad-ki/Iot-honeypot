#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os

MQTT_BROKER = os.getenv("EMQX_HOST", "emqx-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))
TOPICS = ["devices/+/telemetry", "devices/+/status", "$SYS/brokers/+/clients/+/connected"]

def on_connect(client, userdata, flags, rc):
    print(f"✅ Fake subscriber connected to EMQX with result code {rc}")
    for topic in TOPICS:
        client.subscribe(topic)
        print(f"📡 Subscribed to {topic}")

def on_message(client, userdata, msg):
    print(f"📨 Received on {msg.topic}: {msg.payload.decode()}")

def main():
    client = mqtt.Client(client_id=f"sub-fake-{random.randint(1000,9999)}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        print("🤖 Fake subscriber started. Waiting for messages...")
        
        # Keep running
        while True:
            time.sleep(10)
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        client.loop_stop()

if __name__ == "__main__":
    main()
