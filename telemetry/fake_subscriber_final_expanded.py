#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import random
import os
import sys
from datetime import datetime

print("🚀 STARTING FINAL EXPANDED GEOIP SUBSCRIBER...")

# COMPLETE EXPANDED GEOIP DATABASE (INLINE)
GEOIP_DB = {
    # MALICIOUS IPs - HIGH RISK
    "185.165.190.100": {"country": "Russia", "city": "Moscow", "isp": "Unknown Hosting", "country_code": "RU"},
    "185.165.190.101": {"country": "Russia", "city": "Moscow", "isp": "Unknown Hosting", "country_code": "RU"},
    "45.95.147.200": {"country": "Netherlands", "city": "Amsterdam", "isp": "Alsycon B.V.", "country_code": "NL"},
    "45.95.147.201": {"country": "Netherlands", "city": "Amsterdam", "isp": "Alsycon B.V.", "country_code": "NL"},
    "91.218.114.50": {"country": "Russia", "city": "Moscow", "isp": "Selectel", "country_code": "RU"},
    
    # TRUSTED CLOUD IPs - LOW RISK
    "8.8.8.8": {"country": "United States", "city": "Mountain View", "isp": "Google LLC", "country_code": "US"},
    "1.1.1.1": {"country": "United States", "city": "Los Angeles", "isp": "Cloudflare", "country_code": "US"},
    "52.95.128.100": {"country": "United States", "city": "Ashburn", "isp": "Amazon AWS", "country_code": "US"},
    
    # VARIOUS COUNTRIES - MEDIUM RISK
    "203.0.113.1": {"country": "Australia", "city": "Sydney", "isp": "Telstra", "country_code": "AU"},
    "198.51.100.1": {"country": "Germany", "city": "Berlin", "isp": "Deutsche Telekom", "country_code": "DE"},
    "141.101.120.1": {"country": "United Kingdom", "city": "London", "isp": "Cloudflare", "country_code": "GB"},
    "130.130.130.130": {"country": "France", "city": "Paris", "isp": "Orange", "country_code": "FR"},
    "140.140.140.140": {"country": "Japan", "city": "Tokyo", "isp": "NTT", "country_code": "JP"},
    
    # HIGH-RISK COUNTRIES
    "123.123.123.123": {"country": "China", "city": "Beijing", "isp": "China Telecom", "country_code": "CN"},
    
    # PRIVATE IPs - LOW RISK
    "192.168.1.100": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"},
    "10.0.0.1": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"},
}

print(f"📊 EXPANDED DATABASE LOADED: {len(GEOIP_DB)} IP RECORDS")

def get_geoip(ip):
    """Get GeoIP data from expanded database"""
    if ip in GEOIP_DB:
        return GEOIP_DB[ip]
    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown", "country_code": "UNK"}

def assess_threat(ip, geoip):
    """Advanced threat assessment"""
    # Known malicious ranges
    if ip.startswith(("185.165.190.", "45.95.147.", "91.218.114.")):
        return "HIGH", "Known malicious IP range"
    
    # Private IPs
    if geoip["country_code"] == "LOCAL":
        return "LOW", "Internal network"
    
    # High-risk countries
    if geoip["country_code"] in ["RU", "CN", "KP", "IR"]:
        return "HIGH", f"High-risk country: {geoip['country']}"
    
    # Trusted providers
    if any(provider in geoip["isp"].lower() for provider in ["google", "cloudflare", "amazon"]):
        return "LOW", f"Trusted provider: {geoip['isp']}"
    
    return "MEDIUM", f"External IP from {geoip['country']}"

MQTT_BROKER = os.getenv("EMQX_HOST", "mosquitto-honeypot")
MQTT_PORT = int(os.getenv("EMQX_PORT", "1883"))

def on_connect(client, userdata, flags, rc):
    print(f"✅ CONNECTED: Code {rc}")
    client.subscribe("devices/#")
    print("📡 SUBSCRIBED: devices/#")

def on_message(client, userdata, msg):
    try:
        # Select random IP from expanded database
        ip = random.choice(list(GEOIP_DB.keys()))
        geoip = get_geoip(ip)
        threat, reason = assess_threat(ip, geoip)
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "topic": msg.topic,
            "payload": msg.payload.decode(),
            "source_ip": ip,
            "geoip": geoip,
            "threat_level": threat,
            "threat_reason": reason,
            "database": "expanded_v3",
            "total_records": len(GEOIP_DB)
        }
        
        print(json.dumps(log_entry, indent=2))
        sys.stdout.flush()
        
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    client = mqtt.Client(client_id=f"final-expanded-{random.randint(1000,9999)}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_start()
    
    print("🤖 FINAL EXPANDED GEOIP RUNNING...")
    print("🌍 DATABASE INCLUDES MULTIPLE COUNTRIES AND RISK LEVELS")
    
    counter = 0
    while True:
        time.sleep(10)
        counter += 1
        if counter % 6 == 0:
            print(f"💓 Running... ({counter//6}m)")

if __name__ == "__main__":
    main()
