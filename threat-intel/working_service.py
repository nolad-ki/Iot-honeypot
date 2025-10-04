#!/usr/bin/env python3
import sys
import paho.mqtt.client as mqtt
import json
import time
import signal
import threading

print("🚀 Starting Threat Intelligence Service")

sys.path.append(".")

try:
    from threat_intel_service import ThreatIntel
    print("✅ ThreatIntel imported successfully")
except Exception as e:
    print(f"❌ Failed to import ThreatIntel: {e}")
    sys.exit(1)

# Connection event
connection_event = threading.Event()

def on_connect(client, userdata, flags, rc):
    """Callback for when the client receives a CONNACK response from the server."""
    if rc == 0:
        print("✅ Connected to MQTT broker successfully!")
        connection_event.set()
    else:
        print(f"❌ Failed to connect, return code: {rc}")

def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server."""
    try:
        print(f"📨 Received message on topic: {msg.topic}")
        payload = msg.payload.decode()
        print(f"   Payload: {payload}")
        
        # Extract IP address
        ip_address = None
        
        # Try to parse as JSON
        if payload.startswith("{"):
            try:
                data = json.loads(payload)
                ip_address = data.get("ip") or data.get("ip_address") or data.get("src_ip")
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
            print(f"🔍 Analyzing IP address: {ip_address}")
            threat_intel = ThreatIntel()
            result = threat_intel.analyze_ip(ip_address)
            
            # Publish results
            result_topic = f"threat/intel/results"
            client.publish(result_topic, json.dumps(result))
            print(f"✅ Published threat intelligence for {ip_address}")
            print(f"   Results: {json.dumps(result, indent=2)}")
        else:
            print("⚠️  No IP address found in message")
            
    except Exception as e:
        print(f"❌ Error processing message: {e}")
        import traceback
        traceback.print_exc()

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"✅ Subscribed to topic (mid: {mid})")

def on_disconnect(client, userdata, rc):
    print(f"🔌 Disconnected from MQTT broker (code: {rc})")
    connection_event.clear()

# Create MQTT client
print("🔧 Creating MQTT client...")
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

# Set up signal handler for graceful shutdown
def signal_handler(sig, frame):
    print("\n🛑 Shutting down...")
    client.disconnect()
    client.loop_stop()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Connect to MQTT broker
print("🔗 Connecting to MQTT broker at mosquitto:1883...")
try:
    client.connect("mosquitto", 1883, 60)
    print("✅ Connection initiated")
    
    # Subscribe to topics
    topics = ["honeypot/events", "threat/intel", "ips", "cowrie/#"]
    for topic in topics:
        client.subscribe(topic)
        print(f"✅ Subscribed to: {topic}")
    
    # Start the network loop
    print("🔄 Starting MQTT network loop...")
    client.loop_start()
    
    # Wait for connection to be established
    print("⏳ Waiting for connection to be established...")
    if connection_event.wait(timeout=10):
        print("🎯 Threat Intelligence Service is ready and listening for messages!")
        print("   Send MQTT messages to: honeypot/events, threat/intel, ips, or cowrie/#")
        
        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Service interrupted by user")
    else:
        print("❌ Failed to establish connection within timeout period")
        
except Exception as e:
    print(f"❌ Failed to connect to MQTT broker: {e}")
    sys.exit(1)

# Cleanup
print("🧹 Cleaning up...")
client.loop_stop()
client.disconnect()
print("👋 Service stopped")
