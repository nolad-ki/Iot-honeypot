#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
import sys
from datetime import datetime

# Import our expanded database
from expanded_geoip_database import get_expanded_geoip, assess_expanded_threat, EXPANDED_GEOIP_DB

print("🚀 Starting EXPANDED GEOIP subscriber...")
print(f"📊 Using expanded database with {len(EXPANDED_GEOIP_DB)} IP records")

MQTT_BROKER = os.getenv("EMQX_HOST", "mosquitto-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT broker with code: {rc}")
    client.subscribe("devices/#")
    print("📡 Subscribed to devices/#")

def on_message(client, userdata, msg):
    try:
        # Select from all available IPs in our expanded database
        ip_options = list(EXPANDED_GEOIP_DB.keys())
        source_ip = random.choice(ip_options)
        
        # Get expanded GeoIP data
        geoip_data = get_expanded_geoip(source_ip)
        
        # Advanced threat assessment
        threat_level, threat_reason = assess_expanded_threat(source_ip, geoip_data)
        
        # Create comprehensive log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": msg.topic,
            "payload": msg.payload.decode(),
            "source_ip": source_ip,
            "geoip": geoip_data,
            "threat_level": threat_level,
            "threat_reason": threat_reason,
            "enrichment": {
                "version": "expanded_geoip_v2",
                "database_size": len(EXPANDED_GEOIP_DB),
                "has_pre_assessed_risk": "risk" in geoip_data
            }
        }
        
        # Output as JSON
        print(json.dumps(log_entry, indent=2))
        sys.stdout.flush()
        
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def main():
    client = mqtt.Client(client_id=f"expanded-geoip-{random.randint(1000,9999)}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        print("🤖 Expanded GeoIP subscriber running...")
        print("🌍 Database includes IPs from multiple countries and risk levels")
        
        # Keep alive counter
        counter = 0
        while True:
            time.sleep(10)
            counter += 1
            if counter % 6 == 0:  # Every minute
                print(f"💓 Expanded GeoIP subscriber running... ({counter//6} minutes)")
                
    except KeyboardInterrupt:
        print("🛑 Stopping expanded GeoIP subscriber...")
        client.loop_stop()
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

