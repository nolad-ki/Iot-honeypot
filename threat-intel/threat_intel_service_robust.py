#!/usr/bin/env python3
import json
import sys
import os
import time
import random
from datetime import datetime

print("🚀 Starting ROBUST THREAT INTELLIGENCE SERVICE...")

class ThreatIntel:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600
        
    def check_abuseipdb(self, ip_address):
        """Simulated AbuseIPDB check with realistic data"""
        known_malicious = {
            "185.165.190.100": {"abuse_confidence": 95, "total_reports": 150, "country": "Russia"},
            "45.95.147.200": {"abuse_confidence": 88, "total_reports": 89, "country": "Netherlands"},
            "91.218.114.50": {"abuse_confidence": 92, "total_reports": 120, "country": "Russia"},
            "80.94.92.100": {"abuse_confidence": 78, "total_reports": 65, "country": "Bulgaria"}
        }
        
        if ip_address in known_malicious:
            return {
                "source": "abuseipdb_simulated",
                "abuse_confidence": known_malicious[ip_address]["abuse_confidence"],
                "total_reports": known_malicious[ip_address]["total_reports"],
                "country": known_malicious[ip_address]["country"],
                "isp": "Unknown Hosting",
                "last_reported": "2024-01-15T00:00:00Z"
            }
        
        # For trusted IPs, return very low risk
        trusted_ips = ["8.8.8.8", "1.1.1.1", "52.95.128.100"]
        if ip_address in trusted_ips:
            return {
                "source": "abuseipdb_simulated",
                "abuse_confidence": 0,
                "total_reports": 1,
                "country": "United States", 
                "isp": "Trusted Provider",
                "last_reported": "2023-12-01T00:00:00Z"
            }
        
        # For other IPs, return random low-medium risk
        return {
            "source": "abuseipdb_simulated",
            "abuse_confidence": random.randint(5, 25),
            "total_reports": random.randint(0, 10),
            "country": "Various",
            "isp": "Various ISP",
            "last_reported": "2023-11-15T00:00:00Z"
        }
    
    def check_virustotal(self, ip_address):
        """Simulated VirusTotal check"""
        known_malicious = ["185.165.190.100", "45.95.147.200", "91.218.114.50"]
        
        if ip_address in known_malicious:
            return {
                "source": "virustotal_simulated",
                "malicious": random.randint(5, 15),
                "suspicious": random.randint(2, 8),
                "undetected": random.randint(50, 70),
                "harmless": random.randint(10, 20),
                "reputation": -10
            }
        
        return {
            "source": "virustotal_simulated",
            "malicious": 0,
            "suspicious": 0, 
            "undetected": random.randint(60, 80),
            "harmless": random.randint(20, 40),
            "reputation": random.randint(50, 100)
        }
    
    def check_ip(self, ip_address):
        """Check IP against threat intelligence sources"""
        if ip_address in self.cache:
            cached_data, timestamp = self.cache[ip_address]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        threat_data = {
            "ip": ip_address,
            "checked_at": datetime.now().isoformat(),
            "sources": {}
        }
        
        # Check simulated threat intelligence sources
        threat_data["sources"]["abuseipdb"] = self.check_abuseipdb(ip_address)
        threat_data["sources"]["virustotal"] = self.check_virustotal(ip_address)
        
        # Calculate overall threat score
        threat_data["threat_score"] = self.calculate_threat_score(threat_data)
        threat_data["threat_level"] = self.get_threat_level(threat_data["threat_score"])
        
        # Cache the result
        self.cache[ip_address] = (threat_data, time.time())
        
        return threat_data
    
    def calculate_threat_score(self, threat_data):
        """Calculate overall threat score"""
        score = 0
        
        # AbuseIPDB scoring (50% weight)
        abuse_data = threat_data["sources"]["abuseipdb"]
        score += abuse_data["abuse_confidence"] * 0.5
        
        # VirusTotal scoring (50% weight)
        vt_data = threat_data["sources"]["virustotal"]
        score += min(vt_data["malicious"] * 6, 50)  # Up to 50%
        
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
    
    print("🤖 ROBUST THREAT INTELLIGENCE SERVICE READY")
    print("📡 Waiting for log entries...")
    print("💡 Service will run continuously and process incoming data")
    
    # Counter to show service is alive
    counter = 0
    
    try:
        while True:
            # Check for input with timeout
            line = sys.stdin.readline()
            if line:
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
            else:
                # No input received, but keep running
                counter += 1
                if counter % 30 == 0:  # Every ~30 seconds
                    print(f"💓 Threat Intel Service alive... ({counter//30} checks)", file=sys.stderr)
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("🛑 Threat Intelligence Service stopped by user")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

if __name__ == "__main__":
    main()
