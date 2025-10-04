#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os

MQTT_BROKER = os.getenv("EMQX_HOST", "mosquitto-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))
TOPICS = ["devices/+/telemetry", "devices/+/status", "$SYS/brokers/+/clients/+/connected"]

def on_connect(client, userdata, flags, rc):
    print(f"✅ Fake subscriber connected to MQTT honeypot with result code {rc}")
    for topic in TOPICS:
        client.subscribe(topic)
        print(f"📡 Subscribed to {topic}")

def on_message(client, userdata, msg):
    print(f"📨 Received on {msg.topic}: {msg.payload.decode()}")

def connect_with_retry(client, max_retries=10, delay=5):
    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempting to connect to {MQTT_BROKER}:{MQTT_PORT} (attempt {attempt + 1})")
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print(f"✅ Connected to MQTT honeypot on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"❌ Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in {delay} seconds...")
                time.sleep(delay)
    return False

def main():
    client = mqtt.Client(client_id=f"sub-fake-{random.randint(1000,9999)}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    print(f"🤖 Fake subscriber starting...")
    
    if connect_with_retry(client):
        client.loop_start()
        print("🚀 Fake subscriber started. Waiting for messages...")
        
        # Keep running
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("🛑 Stopping fake subscriber...")
        finally:
            client.loop_stop()
    else:
        print("💥 Failed to connect after all retries")

if __name__ == "__main__":
    main()
