#!/usr/bin/env python3
from flask import Flask, jsonify
import sqlite3
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/attacks')
def get_attacks():
    """Get all attacks from the database"""
    try:
        conn = sqlite3.connect('honeypot.db')
        c = conn.cursor()
        c.execute("SELECT * FROM attacks ORDER BY timestamp DESC")
        
        attacks = []
        for row in c.fetchall():
            attacks.append({
                "id": row[0],
                "timestamp": row[1],
                "ip": row[2],
                "service": row[3],
                "username": row[4],
                "password": row[5],
                "command": row[6],
                "data": row[7]
            })
        
        conn.close()
        
        return jsonify({
            "attacks": attacks,
            "timestamp": datetime.now().isoformat(),
            "total_attacks": len(attacks)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get attack statistics"""
    try:
        conn = sqlite3.connect('honeypot.db')
        c = conn.cursor()
        
        # Total attacks
        c.execute("SELECT COUNT(*) FROM attacks")
        total = c.fetchone()[0]
        
        # Attacks by service
        c.execute("SELECT service, COUNT(*) FROM attacks GROUP BY service")
        by_service = {row[0]: row[1] for row in c.fetchall()}
        
        # Recent activity
        c.execute("SELECT COUNT(*) FROM attacks WHERE timestamp > datetime('now', '-1 hour')")
        recent = c.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            "total_attacks": total,
            "attacks_by_service": by_service,
            "recent_attacks": recent,
            "services": list(by_service.keys())
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    return jsonify({"message": "Honeypot API", "status": "running"})

if __name__ == '__main__':
    print("🚀 Fixed API starting on port 5002...")
    print("📊 Using database: honeypot.db")
    app.run(host='0.0.0.0', port=5002, debug=True)
