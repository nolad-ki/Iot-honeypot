#!/usr/bin/env python3
import sqlite3
import time

def sync_databases():
    """Sync data from honeypot-captures.db to honeypot.db"""
    try:
        # Connect to both databases
        source_conn = sqlite3.connect('honeypot-captures.db')
        target_conn = sqlite3.connect('honeypot.db')
        
        source_c = source_conn.cursor()
        target_c = target_conn.cursor()
        
        # Get max ID from target to know what's new
        target_c.execute("SELECT MAX(id) FROM attacks")
        max_target_id = target_c.fetchone()[0] or 0
        
        # Get new records from source
        source_c.execute("SELECT * FROM attacks WHERE id > ?", (max_target_id,))
        new_records = source_c.fetchall()
        
        # Insert new records into target
        for record in new_records:
            target_c.execute('''INSERT INTO attacks (timestamp, ip, service, username, password, command, data)
                             VALUES (?, ?, ?, ?, ?, ?, ?)''', record[1:])
        
        target_conn.commit()
        source_conn.close()
        target_conn.close()
        
        if new_records:
            print(f"✅ Synced {len(new_records)} new attacks to API database")
        return len(new_records)
    except Exception as e:
        print(f"❌ Sync error: {e}")
        return 0

# Run sync
if __name__ == "__main__":
    print("🔄 Starting database sync...")
    synced = sync_databases()
    if synced > 0:
        print(f"🎯 Total in API database: $(sqlite3 honeypot.db 'SELECT COUNT(*) FROM attacks;')")
