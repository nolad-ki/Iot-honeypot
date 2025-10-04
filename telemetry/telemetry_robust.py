#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
import socket
from datetime import datetime

print("🚀 Starting ROBUST telemetry publisher...")

def wait_for_service(host, port, timeout=60):
    """Wait for a service to be available"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                print(f"✅ {host}:{port} is now available!")
                return True
            else:
                print(f"⏳ Waiting for {host}:{port}... ({int(time.time() - start_time)}s)")
        except Exception as e:
            print(f"⚠️  Error checking {host}:{port}: {e}")
        time.sleep(5)
    print(f"❌ Timeout waiting for {host}:{port}")
    return False

def connect_mqtt_with_retry(client, host, port, max_retries=5):
    """Connect to MQTT broker with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"🔗 Connection attempt {attempt + 1} to {host}:{port}...")
            client.connect(host, port, 60)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5  # Increasing backoff
                print(f"🔄 Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
    return False

# Wait for both brokers
print("⏳ Waiting for MQTT brokers to start...")
main_broker_ready = wait_for_service("mosquitto", 1883, timeout=90)
honeypot_broker_ready = wait_for_service("mosquitto-honeypot", 1883, timeout=90)

if not main_broker_ready:
    print("💥 Main broker never became ready, exiting...")
    exit(1)

# Main MQTT client
client = mqtt.Client(client_id=f"pub-{random.randint(1000,9999)}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Successfully connected to main broker!")
    else:
        print(f"❌ Failed to connect to main broker, code: {rc}")

client.on_connect = on_connect

# Connect to main broker
if connect_mqtt_with_retry(client, "mosquitto", 1883):
    client.loop_start()
    print("📡 Starting to publish telemetry data...")
else:
    print("💥 Failed to connect to main broker after all retries")
    exit(1)

# Try to connect to honeypot broker
honeypot_client = None
if honeypot_broker_ready:
    honeypot_client = mqtt.Client(client_id=f"honeypot-{random.randint(1000,9999)}")
    if connect_mqtt_with_retry(honeypot_client, "mosquitto-honeypot", 1883):
        honeypot_client.loop_start()
        print("✅ Also connected to honeypot broker!")
    else:
        print("⚠️  Failed to connect to honeypot broker, continuing without it")
        honeypot_client = None

# Start publishing
counter = 0
try:
    while True:
        data = {
            "device_id": "thermo-001",
            "temperature": round(random.uniform(18.0, 30.0), 2),
            "humidity": round(random.uniform(30.0, 80.0), 1),
            "timestamp": datetime.now().isoformat(),
            "uptime": counter * 5
        }
        
        topic = "devices/thermo-001/telemetry"
        json_data = json.dumps(data)
        
        # Publish to main broker
        client.publish(topic, json_data)
        print(f"📤 To main: {data['temperature']}°C, {data['humidity']}%")
        
        # Publish to honeypot if connected
        if honeypot_client and honeypot_client.is_connected():
            honeypot_client.publish(topic, json_data)
            print(f"📤 To honeypot: {topic}")
        
        counter += 1
        
        if counter % 10 == 0:
            print(f"💓 Published {counter} messages total")
        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("🛑 Stopping telemetry publisher...")
except Exception as e:
    print(f"💥 Unexpected error: {e}")
    import traceback
    traceback.print_exc()
