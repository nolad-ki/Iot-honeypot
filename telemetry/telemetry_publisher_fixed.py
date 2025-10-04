#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
from datetime import datetime

print("🚀 Starting telemetry publisher...")

# Configuration
delay = int(os.getenv("TELEMETRY_DELAY", "5"))
mqtt_broker = os.getenv("MQTT_BROKER", "mosquitto")
mqtt_port = int(os.getenv("MQTT_PORT", "1883"))

print(f"🔧 Configuration:")
print(f"   Broker: {mqtt_broker}:{mqtt_port}")
print(f"   Delay: {delay}s")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Connected to MQTT broker!")
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"📤 Message published (mid: {mid})")

def connect_with_retry(client, broker, port, max_retries=10, retry_delay=5):
    for attempt in range(max_retries):
        try:
            print(f"🔗 Connection attempt {attempt + 1} to {broker}:{port}...")
            client.connect(broker, port, 60)
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
    return False

# Main MQTT client
client = mqtt.Client(client_id=f"pub-{random.randint(1000,9999)}")
client.on_connect = on_connect
client.on_publish = on_publish

# Honeypot MQTT client
honeypot_client = mqtt.Client(client_id=f"honeypot-pub-{random.randint(1000,9999)}")
honeypot_client.on_connect = on_connect
honeypot_client.on_publish = on_publish

try:
    print("🔗 Connecting to main broker...")
    if connect_with_retry(client, mqtt_broker, mqtt_port):
        client.loop_start()
        print("✅ Main broker connected and loop started")
    else:
        print("💥 Failed to connect to main broker after all retries")
        exit(1)
    
    print("🔗 Connecting to honeypot broker...")
    if connect_with_retry(honeypot_client, "mosquitto-honeypot", 1883):
        honeypot_client.loop_start()
        print("✅ Honeypot broker connected and loop started")
    else:
        print("⚠️  Failed to connect to honeypot broker, continuing without it")
    
    print("✅ Both connections established")
    
    device_id = "thermo-001"
    counter = 0
    
    while True:
        # Generate fake telemetry data
        temp = round(random.uniform(18.0, 30.0), 2)
        humidity = round(random.uniform(30.0, 80.0), 1)
        uptime = random.randint(1, 1000000)
        
        payload = {
            "device_id": device_id,
            "ts": datetime.utcnow().isoformat() + "Z",
            "temp_c": temp,
            "humidity": humidity,
            "uptime_s": uptime,
            "ip": "172.21.0.3"
        }
        
        topic = f"devices/{device_id}/telemetry"
        json_payload = json.dumps(payload)
        
        # Publish to main broker
        client.publish(topic, json_payload)
        print(f"📤 To main: {topic} -> Temp: {temp}C, Humidity: {humidity}%")
        
        # Publish to honeypot if connected
        if honeypot_client.is_connected():
            honeypot_client.publish(topic, json_payload)
            print(f"📤 To honeypot: {topic}")
        
        counter += 1
        if counter % 10 == 0:
            print(f"💓 Published {counter} messages so far...")
        
        time.sleep(delay)
        
except Exception as e:
    print(f"💥 Error: {e}")
    import traceback
    traceback.print_exc()
