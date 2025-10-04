#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
from datetime import datetime

print("🚀 Starting telemetry publisher with simple retry...")

# Wait for brokers to be ready
print("⏳ Waiting 15 seconds for brokers to start...")
time.sleep(15)

mqtt_broker = "mosquitto"
mqtt_port = 1883

client = mqtt.Client(client_id=f"pub-{random.randint(1000,9999)}")

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to broker with code: {rc}")

def on_message(client, userdata, msg):
    print(f"Received: {msg.topic} {msg.payload}")

client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"🔗 Connecting to {mqtt_broker}:{mqtt_port}...")
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()
    
    print("📡 Starting to publish telemetry data...")
    
    counter = 0
    while True:
        data = {
            "device_id": "thermo-001",
            "temperature": round(random.uniform(18.0, 30.0), 2),
            "humidity": round(random.uniform(30.0, 80.0), 1),
            "timestamp": datetime.now().isoformat(),
            "uptime": counter * 5
        }
        
        topic = "devices/thermo-001/telemetry"
        client.publish(topic, json.dumps(data))
        print(f"📤 Published to {topic}: {data['temperature']}°C, {data['humidity']}%")
        
        counter += 1
        
        # Also try to connect to honeypot after a few messages
        if counter == 3:
            try:
                honeypot_client = mqtt.Client(client_id=f"honeypot-{random.randint(1000,9999)}")
                honeypot_client.connect("mosquitto-honeypot", 1883, 60)
                honeypot_client.loop_start()
                print("✅ Also connected to honeypot broker")
                # Start publishing to honeypot too
                honeypot_client.publish(topic, json.dumps(data))
                print(f"📤 Also published to honeypot: {topic}")
            except Exception as e:
                print(f"⚠️  Could not connect to honeypot: {e}")
        
        time.sleep(5)
        
except Exception as e:
    print(f"💥 Error: {e}")
    import traceback
    traceback.print_exc()
