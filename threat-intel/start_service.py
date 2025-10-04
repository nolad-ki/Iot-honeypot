#!/usr/bin/env python3
import sys
import paho.mqtt.client as mqtt
import json
import time

print("🚀 Starting Threat Intelligence Service...")

# Add current directory to Python path
sys.path.append(".")

try:
    from threat_intel_service import ThreatIntel
    print("✅ Loaded ThreatIntel class")
except ImportError as e:
    print(f"❌ Failed to import ThreatIntel: {e}")
    sys.exit(1)

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT with code: {rc}")
    # Subscribe to relevant topics
    client.subscribe("honeypot/events")
    client.subscribe("threat/intel")
    client.subscribe("ips")
    client.subscribe("cowrie/#")
    print("✅ Subscribed to topics: honeypot/events, threat/intel, ips, cowrie/#")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        print(f"📨 Received on {msg.topic}")
        
        # Extract IP address from message
        ip_address = None
        
        # Try to parse as JSON
        if payload.startswith("{"):
            try:
                data = json.loads(payload)
                ip_address = data.get("ip") or data.get("ip_address") or data.get("src_ip")
                # For cowrie events
                if not ip_address and "session" in data:
                    ip_address = data["session"].get("peerIP")
            except json.JSONDecodeError:
                pass
        
        # If not JSON or no IP found, check if it's a plain IP
        if not ip_address:
            parts = payload.strip().split(".")
            if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                ip_address = payload.strip()
        
        if ip_address:
            print(f"🔍 Analyzing IP: {ip_address}")
            # Analyze the IP
            threat_intel = ThreatIntel()
            result = threat_intel.analyze_ip(ip_address)
            
            # Publish results
            result_topic = f"threat/intel/results/{ip_address}"
            client.publish(result_topic, json.dumps(result))
            print(f"✅ Published threat intelligence to {result_topic}")
        else:
            print("⚠️  No IP address found in message")
            
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        import traceback
        traceback.print_exc()

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"✅ Subscription confirmed: {mid}")

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

print("🔗 Connecting to MQTT broker...")

# Connect with retry logic
max_attempts = 10
for attempt in range(max_attempts):
    try:
        client.connect("mosquitto", 1883, 60)
        print("✅ Successfully connected to MQTT broker")
        break
    except Exception as e:
        print(f"Attempt {attempt + 1}/{max_attempts} failed: {e}")
        if attempt < max_attempts - 1:
            time.sleep(2)
else:
    print("❌ Failed to connect to MQTT after all attempts")
    sys.exit(1)

print("🎯 Threat Intelligence Service is ready and listening for messages...")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Service stopped by user")
except Exception as e:
    print(f"Service error: {e}")
