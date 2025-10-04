#!/usr/bin/env python3
"""
Telemetry publisher:
 - publishes JSON messages to MQTT topic devices/<device_id>/telemetry
 - appends each JSON line to a host-mounted logfile (LOGFILE)
"""
import time, json, random, socket, os
from datetime import datetime
import paho.mqtt.client as mqtt
import os

delay = int(os.getenv("TELEMETRY_DELAY", "5"))
BROKER = os.getenv("MQTT_HOST", "mosquitto")
PORT = int(os.getenv("MQTT_PORT", 1883))
DEVICE_ID = os.getenv("DEVICE_ID", "thermo-001")
TOPIC = f"devices/{DEVICE_ID}/telemetry"
LOGFILE = os.getenv("LOGFILE", "/cowrie-data/telemetry.log")
INTERVAL = int(os.getenv("INTERVAL", 5))

client = mqtt.Client(client_id=f"pub-{random.randint(1000,9999)}")

# Wait until broker is available (resilient start)
while True:
    try:
        client.connect(BROKER, PORT, 60)
        break
    except Exception as e:
        print('MQTT connect failed, retrying...', e)
        time.sleep(delay)

def make_reading():
    return {
        "device_id": DEVICE_ID,
        "ts": datetime.utcnow().isoformat() + "Z",
        "temp_c": round(18 + random.random()*10, 2),
        "humidity": round(30 + random.random()*40, 1),
        "uptime_s": random.randint(1000, 999999),
        "ip": socket.gethostbyname(socket.gethostname())
    }

try:
    while True:
        payload = json.dumps(make_reading(), separators=(',', ':'))
        try:
            client.publish(TOPIC, payload, qos=0)
        except Exception as e:
            print('Publish error:', e)
        # append to logfile (atomic-ish append)
        try:
            with open(LOGFILE, "a") as f:
                f.write(payload + "\\n")
        except Exception as e:
            print('Log write error:', e)
        print("Published", payload)
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    try:
        client.disconnect()
    except:
        pass
    print("Telemetry publisher stopped.")
def main():
    print("🚀 Starting telemetry publisher...")
    
    mqtt_broker = os.getenv("MQTT_BROKER", "mosquitto")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))
    
    print(f"🔧 Configuration: {mqtt_broker}:{mqtt_port}")
    
    client = mqtt.Client(client_id=f"pub-{random.randint(1000,9999)}")
    
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("✅ Connected to MQTT broker!")
        else:
            print(f"❌ Failed to connect, return code {rc}")
    
    client.on_connect = on_connect
    
    try:
        print(f"🔗 Connecting to {mqtt_broker}:{mqtt_port}...")
        client.connect(mqtt_broker, mqtt_port, 60)
        client.loop_start()
        print("✅ MQTT loop started")
        
        device_id = "thermo-001"
        print(f"📡 Starting to publish telemetry for device: {device_id}")
        
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
            client.publish(topic, json.dumps(payload))
            print(f"📤 Published: {topic} -> {payload}")
            
            time.sleep(delay)
            
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()
