#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
import requests
from datetime import datetime

print("🚀 Starting ENRICHED fake subscriber...")

def get_simple_geoip(ip):
    """Simple GeoIP lookup"""
    try:
        response = requests.get(f"http://ipapi.co/{ip}/json/", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country_name", "Unknown"),
                "city": data.get("city", "Unknown"),
                "isp": data.get("org", "Unknown")
            }
    except:
        pass
    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}

MQTT_BROKER = os.getenv("EMQX_HOST", "mosquitto-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT broker with code: {rc}")
    client.subscribe("devices/#")
    print("📡 Subscribed to devices/#")

def on_message(client, userdata, msg):
    # Create enriched log entry
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": msg.topic,
        "payload": msg.payload.decode(),
        "source_ip": "attacker_unknown",  # In real scenario, you'd get this from connection
        "type": "mqtt_message"
    }
    
    # Add basic enrichment (in real scenario, you'd have the actual source IP)
    sample_ips = ["185.165.190.100", "45.95.147.200", "192.168.1.100", "8.8.8.8"]
    fake_ip = random.choice(sample_ips)
    log_entry["source_ip"] = fake_ip
    log_entry["geoip"] = get_simple_geoip(fake_ip)
    
    # Threat assessment
    if any(suspicious in fake_ip for suspicious in ["185.165.190", "45.95.147"]):
        log_entry["threat_level"] = "HIGH"
        log_entry["threat_reason"] = "Known malicious IP range"
    elif fake_ip.startswith("192.168."):
        log_entry["threat_level"] = "LOW" 
        log_entry["threat_reason"] = "Internal network"
    else:
        log_entry["threat_level"] = "MEDIUM"
        log_entry["threat_reason"] = "External IP"
    
    print(json.dumps(log_entry))
    sys.stdout.flush()

def main():
    client = mqtt.Client(client_id=f"enriched-sub-{random.randint(1000,9999)}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    print("🤖 Enriched subscriber running. Logging to stdout...")
    
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        client.loop_stop()

if __name__ == "__main__":
    import sys
    main()
