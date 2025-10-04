#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
import sys
from datetime import datetime

print("🚀 Starting ENRICHED fake subscriber with LOCAL GEOIP...")

# Local GeoIP database (no external API calls)
LOCAL_GEOIP_DB = {
    "8.8.8.8": {"country": "United States", "city": "Mountain View", "isp": "Google LLC", "country_code": "US"},
    "1.1.1.1": {"country": "United States", "city": "Los Angeles", "isp": "Cloudflare", "country_code": "US"},
    "185.165.190.100": {"country": "Russia", "city": "Moscow", "isp": "Unknown Hosting", "country_code": "RU"},
    "45.95.147.200": {"country": "Netherlands", "city": "Amsterdam", "isp": "Unknown Hosting", "country_code": "NL"},
    "192.168.1.100": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"},
    "10.0.0.1": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"},
    "172.16.0.1": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"},
    "203.0.113.1": {"country": "Australia", "city": "Sydney", "isp": "Telstra", "country_code": "AU"},
    "198.51.100.1": {"country": "Germany", "city": "Berlin", "isp": "Deutsche Telekom", "country_code": "DE"},
    "141.101.120.1": {"country": "United Kingdom", "city": "London", "isp": "Cloudflare", "country_code": "GB"}
}

# Known malicious IP ranges (expanded)
MALICIOUS_RANGES = [
    "185.165.190.", "45.95.147.", "91.218.114.", "80.94.92.",
    "192.241.200.", "45.142.214.", "185.220.101.", "45.137.21.",
    "5.188.206.", "193.142.146.", "194.87.139.", "195.2.76."
]

# Known cloud providers (usually safe)
CLOUD_PROVIDERS = ["google", "cloudflare", "amazon", "microsoft", "digitalocean", "linode"]

def get_local_geoip(ip_address):
    """Get GeoIP information from local database"""
    # Exact match
    if ip_address in LOCAL_GEOIP_DB:
        return LOCAL_GEOIP_DB[ip_address]
    
    # Private IP ranges
    if ip_address.startswith(("10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.", "192.168.")):
        return {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"}
    
    # Default for unknown IPs
    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown", "country_code": "UNK"}

def assess_threat_level(ip_address, geoip_data):
    """Advanced threat assessment using multiple factors"""
    
    # Check known malicious ranges
    for malicious_range in MALICIOUS_RANGES:
        if ip_address.startswith(malicious_range):
            return "HIGH", "Known malicious IP range"
    
    # Private IPs are low threat
    if geoip_data["country_code"] == "LOCAL":
        return "LOW", "Internal network IP"
    
    # Check country risk (simplified)
    high_risk_countries = ["RU", "CN", "KP", "IR", "SY"]
    if geoip_data["country_code"] in high_risk_countries:
        return "HIGH", f"High-risk country: {geoip_data['country']}"
    
    # Check ISP/Organization
    isp_lower = geoip_data["isp"].lower()
    if any(cloud in isp_lower for cloud in CLOUD_PROVIDERS):
        return "LOW", f"Trusted cloud provider: {geoip_data['isp']}"
    
    # Unknown hosting providers
    if "unknown" in isp_lower or "hosting" in isp_lower:
        return "MEDIUM", "Unknown hosting provider"
    
    # Default for other external IPs
    return "MEDIUM", f"External IP from {geoip_data['country']}"

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
        
        # Select a realistic source IP
        sample_ips = list(LOCAL_GEOIP_DB.keys()) + ["203.0.113.5", "198.51.100.10", "141.101.120.15"]
        fake_ip = random.choice(sample_ips)
        log_entry["source_ip"] = fake_ip
        
        # Get local GeoIP data (no external API calls)
        log_entry["geoip"] = get_local_geoip(fake_ip)
        
        # Advanced threat assessment
        threat_level, threat_reason = assess_threat_level(fake_ip, log_entry["geoip"])
        log_entry["threat_level"] = threat_level
        log_entry["threat_reason"] = threat_reason
        
        # Add additional context
        log_entry["analysis"] = {
            "geoip_source": "local_database",
            "has_malicious_intent": threat_level in ["HIGH", "MEDIUM"],
            "recommended_action": "monitor" if threat_level == "LOW" else "investigate"
        }
        
        # Print as JSON for easy parsing
        print(json.dumps(log_entry, indent=2))
        sys.stdout.flush()
        
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    client = mqtt.Client(client_id=f"geoip-sub-{random.randint(1000,9999)}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        print("🤖 Local GeoIP subscriber running. Database loaded with realistic data...")
        print(f"📊 Local database has {len(LOCAL_GEOIP_DB)} IP records")
        print("🌍 No external API calls - all GeoIP data is local!")
        
        # Keep alive counter
        counter = 0
        while True:
            time.sleep(10)
            counter += 1
            if counter % 6 == 0:  # Every minute
                print(f"💓 Local GeoIP subscriber running... ({counter//6} minutes)")
                
    except KeyboardInterrupt:
        print("🛑 Stopping local GeoIP subscriber...")
        client.loop_stop()
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
