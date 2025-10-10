#!/usr/bin/env python3
import sqlite3
import sys
import json
from datetime import datetime

def log_attack(service, ip, username="", password="", command="", data=""):
    conn = sqlite3.connect('honeypot-captures.db')
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute('''INSERT INTO attacks (timestamp, ip, service, username, password, command, data)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
             (timestamp, ip, service, username, password, command, data))
    conn.commit()
    conn.close()
    print(f"📝 LOGGED: {service} - {username}:{password} - {command}")

# Test it
if __name__ == "__main__":
    log_attack("test", "127.0.0.1", "testuser", "testpass", "test command")
    print("✅ Database logger ready!")
