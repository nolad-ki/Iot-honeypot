#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
import socket

print("🚀 Starting fake subscriber with debug info...")

MQTT_BROKER = os.getenv("EMQX_HOST", "mosquitto-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))
TOPICS = ["devices/+/telemetry", "devices/+/status", "$SYS/brokers/+/clients/+/connected"]

print(f"🔧 Configuration:")
print(f"   Broker: {MQTT_BROKER}")
print(f"   Port: {MQTT_PORT}")
print(f"   Topics: {TOPICS}")

# Test DNS resolution first
try:
    ip = socket.gethostbyname(MQTT_BROKER)
    print(f"✅ DNS resolved {MQTT_BROKER} -> {ip}")
except Exception as e:
    print(f"❌ DNS resolution failed: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ Successfully connected to MQTT broker!")
        for topic in TOPICS:
            client.subscribe(topic)
            print(f"📡 Subscribed to {topic}")
    else:
        print(f"❌ Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print(f"📨 RECEIVED MESSAGE:")
    print(f"   Topic: {msg.topic}")
    print(f"   Payload: {msg.payload.decode()}")
    print(f"   QoS: {msg.qos}")

def on_disconnect(client, userdata, rc):
    print(f"🔌 Disconnected from broker with code: {rc}")

def main():
    client_id = f"sub-fake-{random.randint(1000,9999)}"
    print(f"🆔 Client ID: {client_id}")
    
    client = mqtt.Client(client_id=client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    # Set last will and testament
    client.will_set("devices/fake-subscriber/status", "offline", retain=True)
    
    print(f"🔗 Attempting to connect to {MQTT_BROKER}:{MQTT_PORT}...")
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print("✅ Connection attempt completed, starting loop...")
        client.loop_start()
        
        # Publish that we're online
        client.publish("devices/fake-subscriber/status", "online", retain=True)
        print("📤 Published online status")
        
        print("🚀 Fake subscriber is running and waiting for messages...")
        
        # Keep running and show heartbeat
        counter = 0
        while True:
            time.sleep(10)
            counter += 1
            if counter % 6 == 0:  # Every minute
                print(f"💓 Still running... ({counter//6} minutes)")
                
    except Exception as e:
        print(f"💥 Critical error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
