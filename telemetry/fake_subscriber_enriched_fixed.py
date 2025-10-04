#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
import requests
import sys
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
                "isp": data.get("org", "Unknown"),
                "country_code": data.get("country_code", "Unknown")
            }
    except Exception as e:
        print(f"GeoIP lookup failed: {e}")
    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown", "country_code": "Unknown"}

MQTT_BROKER = os.getenv("EMQX_HOST", "mosquitto-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT broker with code: {rc}")
    client.subscribe("devices/#")
    print("📡 Subscribed to devices/#")

def on_message(client, userdata, msg):
    try:
        # Create enriched log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": msg.topic,
            "payload": msg.payload.decode(),
            "type": "mqtt_message",
            "message_size": len(msg.payload)
        }
        
        # Add fake source IP for demonstration
        sample_ips = [
            "185.165.190.100",  # Known suspicious
            "45.95.147.200",    # Known suspicious  
            "192.168.1.100",    # Internal
            "8.8.8.8",          # Google DNS
            "1.1.1.1"           # Cloudflare
        ]
        fake_ip = random.choice(sample_ips)
        log_entry["source_ip"] = fake_ip
        
        # Add GeoIP enrichment
        log_entry["geoip"] = get_simple_geoip(fake_ip)
        
        # Add threat assessment
        if any(suspicious in fake_ip for suspicious in ["185.165.190", "45.95.147"]):
            log_entry["threat_level"] = "HIGH"
            log_entry["threat_reason"] = "Known malicious IP range"
        elif fake_ip.startswith(("192.168.", "10.", "172.16.")):
            log_entry["threat_level"] = "LOW" 
            log_entry["threat_reason"] = "Internal network IP"
        else:
            log_entry["threat_level"] = "MEDIUM"
            log_entry["threat_reason"] = "External IP"
        
        # Print as JSON for easy parsing
        print(json.dumps(log_entry, indent=2))
        sys.stdout.flush()
        
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    client = mqtt.Client(client_id=f"enriched-sub-{random.randint(1000,9999)}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        print("🤖 Enriched subscriber running. Waiting for messages...")
        
        # Keep alive counter
        counter = 0
        while True:
            time.sleep(10)
            counter += 1
            if counter % 6 == 0:  # Every minute
                print(f"💓 Enriched subscriber still running... ({counter//6} minutes)")
                
    except KeyboardInterrupt:
        print("🛑 Stopping enriched subscriber...")
        client.loop_stop()
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
