#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime
import random

class HoneypotAPIHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        # Add CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if self.path == '/api/stats':
            response = {
                'total_attacks': 1247,
                'attacks_today': random.randint(40, 60),
                'unique_attackers': 156,
                'honeypots_active': 5,
                'threat_level': 'High'
            }
        elif self.path == '/api/attacks':
            attack_types = ['SSH Brute Force', 'Port Scanning', 'FTP Login Attempt', 
                           'HTTP Request', 'SQL Injection', 'RDP Connection']
            countries = ['United States', 'China', 'Russia', 'Germany', 'Brazil', 'India']
            
            attacks = []
            for i in range(random.randint(5, 15)):
                attacks.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': random.choice(attack_types),
                    'source_ip': f'192.168.1.{random.randint(1, 255)}',
                    'details': f'Attack attempt detected from {random.choice(countries)}',
                    'honeypot': random.choice(['ssh-honeypot', 'ftp-honeypot', 'http-honeypot'])
                })
            
            response = {
                'attacks': attacks,
                'total_attacks': len(attacks),
                'timestamp': datetime.now().isoformat()
            }
        else:
            response = {'message': 'Honeypot API is running', 'status': 'active'}
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

print("Starting Simple Honeypot API on http://localhost:5000")
server = HTTPServer(('0.0.0.0', 5000), HoneypotAPIHandler)
server.serve_forever()
