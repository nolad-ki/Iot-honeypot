#!/usr/bin/env python3
import json
import sys
import os
import requests
import time
from datetime import datetime

print("🚀 Starting Real-time Threat Intelligence Service...")

# Configuration
ABUSEIPDB_API_KEY = os.getenv('ABUSEIPDB_API_KEY', '')
VIRUSTOTAL_API_KEY = os.getenv('VIRUSTOTAL_API_KEY', '')

class ThreatIntel:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache
        
    def check_abuseipdb(self, ip_address):
        """Check IP against AbuseIPDB"""
        if not ABUSEIPDB_API_KEY:
            return {"error": "No AbuseIPDB API key configured"}
            
        try:
            url = "https://api.abuseipdb.com/api/v2/check"
            headers = {
                'Key': ABUSEIPDB_API_KEY,
                'Accept': 'application/json'
            }
            params = {
                'ipAddress': ip_address,
                'maxAgeInDays': 90
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "abuseipdb",
                    "abuse_confidence": data['data'].get('abuseConfidenceScore', 0),
                    "total_reports": data['data'].get('totalReports', 0),
                    "country": data['data'].get('countryCode', 'Unknown'),
                    "isp": data['data'].get('isp', 'Unknown'),
                    "last_reported": data['data'].get('lastReportedAt', 'Never')
                }
        except Exception as e:
            return {"error": f"AbuseIPDB check failed: {e}"}
        
        return {"error": "AbuseIPDB check failed"}
    
    def check_virustotal(self, ip_address):
        """Check IP against VirusTotal"""
        if not VIRUSTOTAL_API_KEY:
            return {"error": "No VirusTotal API key configured"}
            
        try:
            url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip_address}"
            headers = {
                'x-apikey': VIRUSTOTAL_API_KEY
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                stats = data['data']['attributes']['last_analysis_stats']
                return {
                    "source": "virustotal",
                    "malicious": stats.get('malicious', 0),
                    "suspicious": stats.get('suspicious', 0),
                    "undetected": stats.get('undetected', 0),
                    "harmless": stats.get('harmless', 0),
                    "reputation": data['data']['attributes'].get('reputation', 0),
                    "country": data['data']['attributes'].get('country', 'Unknown')
                }
        except Exception as e:
            return {"error": f"VirusTotal check failed: {e}"}
        
        return {"error": "VirusTotal check failed"}
    
    def check_ip(self, ip_address):
        """Check IP against all available threat intelligence sources"""
        # Check cache first
        if ip_address in self.cache:
            cached_data, timestamp = self.cache[ip_address]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        print(f"🔍 Checking threat intelligence for {ip_address}...")
        
        threat_data = {
            "ip": ip_address,
            "checked_at": datetime.now().isoformat(),
            "sources": {}
        }
        
        # Check AbuseIPDB
        abuse_result = self.check_abuseipdb(ip_address)
        threat_data["sources"]["abuseipdb"] = abuse_result
        
        # Check VirusTotal
        vt_result = self.check_virustotal(ip_address)
        threat_data["sources"]["virustotal"] = vt_result
        
        # Calculate overall threat score
        threat_data["threat_score"] = self.calculate_threat_score(threat_data)
        threat_data["threat_level"] = self.get_threat_level(threat_data["threat_score"])
        
        # Cache the result
        self.cache[ip_address] = (threat_data, time.time())
        
        return threat_data
    
    def calculate_threat_score(self, threat_data):
        """Calculate overall threat score from multiple sources"""
        score = 0
        
        # AbuseIPDB scoring
        abuse_data = threat_data["sources"].get("abuseipdb", {})
        if "abuse_confidence" in abuse_data:
            score += abuse_data["abuse_confidence"] * 0.5  # 50% weight
        
        # VirusTotal scoring
        vt_data = threat_data["sources"].get("virustotal", {})
        if "malicious" in vt_data:
            malicious = vt_data["malicious"]
            if malicious > 0:
                score += min(malicious * 10, 50)  # Up to 50% weight
        
        return min(score, 100)
    
    def get_threat_level(self, score):
        """Convert threat score to level"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        elif score >= 20:
            return "LOW"
        else:
            return "INFO"

def main():
    threat_intel = ThreatIntel()
    
    print("🤖 Threat Intelligence Service Ready")
    print("📡 Listening for IP addresses on stdin...")
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if line:
                try:
                    # Parse the log entry
                    log_entry = json.loads(line)
                    source_ip = log_entry.get("source_ip")
                    
                    if source_ip and source_ip not in ["LOCAL", "UNK", "Private"]:
                        # Check threat intelligence
                        threat_info = threat_intel.check_ip(source_ip)
                        
                        # Merge with original log entry
                        enriched_entry = {**log_entry, "threat_intel": threat_info}
                        
                        # Output enriched entry
                        print(json.dumps(enriched_entry))
                        sys.stdout.flush()
                    else:
                        # Pass through entries without valid IPs
                        print(line)
                        sys.stdout.flush()
                        
                except json.JSONDecodeError:
                    # Pass through non-JSON lines
                    print(line)
                    sys.stdout.flush()
                    
    except KeyboardInterrupt:
        print("🛑 Threat Intelligence Service stopped")

if __name__ == "__main__":
    main()
