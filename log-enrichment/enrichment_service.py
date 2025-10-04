#!/usr/bin/env python3
import json
import sys
import socket
import requests
import time
from datetime import datetime

def get_geoip_info(ip_address):
    """Get GeoIP information for an IP address"""
    try:
        # Using ipapi.co free service (1000 requests/day)
        response = requests.get(f"http://ipapi.co/{ip_address}/json/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "country": data.get("country_name", "Unknown"),
                "city": data.get("city", "Unknown"),
                "region": data.get("region", "Unknown"),
                "isp": data.get("org", "Unknown"),
                "country_code": data.get("country_code", "Unknown")
            }
    except Exception as e:
        print(f"GeoIP lookup failed for {ip_address}: {e}")
    return {"country": "Unknown", "city": "Unknown", "region": "Unknown", "isp": "Unknown"}

def check_threat_intelligence(ip_address):
    """Check if IP is in threat intelligence databases"""
    # Simple check - in production, use services like AbuseIPDB, VirusTotal, etc.
    suspicious_ranges = [
        "185.165.190.", "45.95.147.", "91.218.114.", "80.94.92.",
        "192.241.200.", "45.142.214.", "185.220.101.", "45.137.21."
    ]
    
    for range in suspicious_ranges:
        if ip_address.startswith(range):
            return {"threat_level": "HIGH", "reason": "Known malicious range"}
    
    # Check if private IP
    if ip_address.startswith(("10.", "172.16.", "192.168.", "127.")):
        return {"threat_level": "LOW", "reason": "Private IP"}
    
    return {"threat_level": "UNKNOWN", "reason": "No threat data"}

def enrich_log_entry(log_entry):
    """Enrich a log entry with GeoIP and threat intelligence"""
    try:
        # Extract IP from log entry
        ip_address = None
        
        # Try to find IP in the log entry
        if "ip" in log_entry:
            ip_address = log_entry["ip"]
        elif "source_ip" in log_entry:
            ip_address = log_entry["source_ip"]
        elif "client_ip" in log_entry:
            ip_address = log_entry["client_ip"]
        
        if ip_address:
            # Get enrichment data
            geoip_data = get_geoip_info(ip_address)
            threat_data = check_threat_intelligence(ip_address)
            
            # Add enrichment to log entry
            log_entry["geoip"] = geoip_data
            log_entry["threat_intel"] = threat_data
            log_entry["enriched_at"] = datetime.now().isoformat()
        
        return log_entry
        
    except Exception as e:
        print(f"Enrichment failed: {e}")
        return log_entry

def main():
    print("🚀 Starting Log Enrichment Service...")
    print("📡 Listening for log entries on stdin...")
    
    try:
        while True:
            # Read from stdin
            line = sys.stdin.readline()
            if not line:
                break
                
            if line.strip():
                try:
                    # Parse JSON log entry
                    log_entry = json.loads(line.strip())
                    
                    # Enrich the log entry
                    enriched_entry = enrich_log_entry(log_entry)
                    
                    # Output enriched entry
                    print(json.dumps(enriched_entry))
                    sys.stdout.flush()
                    
                except json.JSONDecodeError:
                    # If it's not JSON, just pass it through
                    print(line.strip())
                    sys.stdout.flush()
                    
    except KeyboardInterrupt:
        print("🛑 Enrichment service stopped")

if __name__ == "__main__":
    main()
