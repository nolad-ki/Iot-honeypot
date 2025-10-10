#!/usr/bin/env python3
import sqlite3
import json
from datetime import datetime

def log_attack(service, ip, username="", password="", command="", data=""):
    """Universal function for all honeypots to log to database"""
    try:
        conn = sqlite3.connect('honeypot-captures.db')
        c = conn.cursor()
        timestamp = datetime.now().isoformat()
        
        c.execute('''INSERT INTO attacks (timestamp, ip, service, username, password, command, data)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (timestamp, ip, service, username, password, command, data))
        conn.commit()
        conn.close()
        
        print(f"🎯 DATABASE CAPTURED: {service} | {ip} | {username}:{password} | {command}")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

# Test the module
if __name__ == "__main__":
    log_attack("test", "127.0.0.1", "testuser", "testpass", "module test")
    print("✅ Database module ready!")
