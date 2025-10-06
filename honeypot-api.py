from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import json
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

def get_honeypot_logs(service_name):
    """Get recent logs from a honeypot container"""
    try:
        result = subprocess.run([
            'docker', 'logs', service_name, '--tail', '50'
        ], capture_output=True, text=True, timeout=10)
        return result.stdout.split('\n')[-20:]  # Last 20 lines
    except:
        return []

def parse_ftp_attacks(logs):
    """Parse FTP honeypot for login attempts"""
    attacks = []
    for line in logs:
        if 'USER' in line or 'PASS' in line:
            attacks.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'FTP Login Attempt',
                'source_ip': 'Unknown',
                'details': line.strip(),
                'honeypot': 'ftp-honeypot'
            })
    return attacks

def parse_http_attacks(logs):
    """Parse HTTP honeypot for web attacks"""
    attacks = []
    for line in logs:
        if 'GET' in line or 'POST' in line:
            attacks.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'HTTP Request',
                'source_ip': 'Unknown', 
                'details': line.strip(),
                'honeypot': 'http-honeypot'
            })
    return attacks

def parse_ssh_attacks(logs):
    """Parse SSH honeypot for connection attempts"""
    attacks = []
    for line in logs:
        if 'connection' in line.lower() or 'login' in line.lower():
            attacks.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'SSH Connection',
                'source_ip': 'Unknown',
                'details': line.strip(),
                'honeypot': 'ssh-honeypot'
            })
    return attacks

@app.route('/api/attacks')
def get_attacks():
    """Get all attacks from all honeypots"""
    all_attacks = []
    
    # FTP Honeypot
    ftp_logs = get_honeypot_logs('ftp-honeypot')
    all_attacks.extend(parse_ftp_attacks(ftp_logs))
    
    # HTTP Honeypot  
    http_logs = get_honeypot_logs('http-honeypot')
    all_attacks.extend(parse_http_attacks(http_logs))
    
    # SSH Honeypot
    ssh_logs = get_honeypot_logs('ssh-honeypot')
    all_attacks.extend(parse_ssh_attacks(ssh_logs))
    
    # RDP Honeypot (basic)
    rdp_attacks = [{
        'timestamp': datetime.now().isoformat(),
        'type': 'RDP Connection',
        'source_ip': 'Unknown',
        'details': 'RDP port scan detected',
        'honeypot': 'rdp-honeypot'
    }] if len(all_attacks) > 0 else []
    all_attacks.extend(rdp_attacks)
    
    # MySQL Honeypot (basic)
    mysql_attacks = [{
        'timestamp': datetime.now().isoformat(), 
        'type': 'MySQL Connection',
        'source_ip': 'Unknown',
        'details': 'Database connection attempt',
        'honeypot': 'mysql-honeypot'
    }] if len(all_attacks) > 0 else []
    all_attacks.extend(mysql_attacks)
    
    return jsonify({
        'attacks': all_attacks[-50:],  # Last 50 attacks
        'total_attacks': len(all_attacks),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
def get_stats():
    """Get honeypot statistics"""
    stats = {
        'total_attacks': 0,
        'attacks_today': 0,
        'unique_attackers': 0,
        'honeypots_active': 5,
        'threat_level': 'Medium'
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
