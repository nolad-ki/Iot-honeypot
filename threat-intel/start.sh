#!/bin/sh
# Install paho-mqtt
pip install paho-mqtt

# Create a simple Python script that connects to MQTT
python3 -c "
import sys
import paho.mqtt.client as mqtt
import json
import time

print('Starting Threat Intelligence Service...')

# Add current directory to path
sys.path.append('.')

try:
    from threat_intel_service import ThreatIntel
    print('Loaded ThreatIntel class')
except ImportError as e:
    print(f'Error loading ThreatIntel: {e}')
    sys.exit(1)

def on_connect(client, userdata, flags, rc):
    print(f'Connected to MQTT with code: {rc}')
    if rc == 0:
        client.subscribe('honeypot/events')
        client.subscribe('threat/intel')
        client.subscribe('ips')
        print('Subscribed to topics')
    else:
        print(f'Connection failed: {rc}')

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f'Message on {msg.topic}: {payload[:100]}')
        
        # Extract IP address
        ip = None
        if payload.startswith('{'):
            try:
                data = json.loads(payload)
                ip = data.get('ip') or data.get('ip_address')
            except:
                pass
        elif '.' in payload:
            parts = payload.strip().split('.')
            if len(parts) == 4 and all(p.isdigit() for p in parts):
                ip = payload.strip()
        
        if ip:
            print(f'Analyzing IP: {ip}')
            result = ThreatIntel().analyze_ip(ip)
            print(f'Results: {result}')
            client.publish('threat/intel/results', json.dumps(result))
    except Exception as e:
        print(f'Error processing message: {e}')

# Connect to MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print('Connecting to MQTT broker...')
for i in range(10):
    try:
        client.connect('mosquitto', 1883, 60)
        print('Connected successfully!')
        client.loop_forever()
        break
    except Exception as e:
        print(f'Connection attempt {i+1} failed: {e}')
        time.sleep(2)
else:
    print('Failed to connect after 10 attempts')
    sys.exit(1)
"
