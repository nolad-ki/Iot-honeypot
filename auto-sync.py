#!/usr/bin/env python3
import sqlite3
import time
import sys

def sync_databases():
    try:
        source_conn = sqlite3.connect('honeypot-captures.db')
        target_conn = sqlite3.connect('honeypot.db')
        
        source_c = source_conn.cursor()
        target_c = target_conn.cursor()
        
        target_c.execute("SELECT MAX(id) FROM attacks")
        max_target_id = target_c.fetchone()[0] or 0
        
        source_c.execute("SELECT * FROM attacks WHERE id > ?", (max_target_id,))
        new_records = source_c.fetchall()
        
        for record in new_records:
            target_c.execute('''INSERT INTO attacks (timestamp, ip, service, username, password, command, data)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''', record[1:])
        
        target_conn.commit()
        source_conn.close()
        target_conn.close()
        
        if new_records:
            print(f"🔄 Synced {len(new_records)} new attacks")
        return len(new_records)
    except Exception as e:
        print(f"❌ Sync error: {e}")
        return 0

print("🔄 Starting continuous database sync (Ctrl+C to stop)...")
while True:
    sync_databases()
    time.sleep(5)  # Sync every 5 seconds
