#!/usr/bin/env python3
from flask import Flask, request, jsonify
import json
import time
import socket

app = Flask(__name__)

# Store attack data
attacks = []

@app.route('/')
def index():
    log_attack(request, "Homepage access")
    return '''
    <html>
        <head><title>Company Admin Panel</title></head>
        <body>
            <h1>Company Internal Admin Panel</h1>
            <p>Please login to access sensitive data</p>
            <form action="/login" method="post">
                Username: <input type="text" name="username"><br>
                Password: <input type="password" name="password"><br>
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    
    log_attack(request, f"Login attempt - User: {username}, Pass: {password}")
    
    # Always fail login to keep them trying
    return "Invalid credentials. Please try again.", 401

@app.route('/admin')
def admin():
    log_attack(request, "Admin panel access attempt")
    return "Access denied. Administrator privileges required.", 403

@app.route('/phpmyadmin')
def phpmyadmin():
    log_attack(request, "phpMyAdmin access attempt")
    return "404 Not Found", 404

@app.route('/wp-admin')
def wp_admin():
    log_attack(request, "WordPress admin access attempt")
    return "404 Not Found", 404

@app.route('/.env')
def env_file():
    log_attack(request, ".env file access attempt")
    return "404 Not Found", 404

@app.route('/api/users')
def api_users():
    log_attack(request, "API endpoint access attempt")
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/shell', methods=['GET', 'POST'])
def shell():
    log_attack(request, "Web shell access attempt")
    return "404 Not Found", 404

@app.route('/<path:path>')
def catch_all(path):
    log_attack(request, f"Unknown path access: /{path}")
    return "404 Not Found", 404

def log_attack(request, description):
    attacker_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')
    method = request.method
    path = request.path
    
    attack_data = {
        'timestamp': time.time(),
        'ip': attacker_ip,
        'user_agent': user_agent,
        'method': method,
        'path': path,
        'description': description,
        'headers': dict(request.headers)
    }
    
    attacks.append(attack_data)
    
    # Print to console (Docker logs)
    print(f"🚨 HTTP Attack: {attacker_ip} - {description}")
    print(f"   Path: {path}, Method: {method}")
    print(f"   User-Agent: {user_agent}")
    
    # Also publish to MQTT for threat intelligence
    try:
        import paho.mqtt.publish as publish
        mqtt_msg = {
            'type': 'http_attack',
            'ip': attacker_ip,
            'path': path,
            'method': method,
            'description': description,
            'timestamp': time.time()
        }
        publish.single('honeypot/events', json.dumps(mqtt_msg), hostname='mosquitto')
    except:
        pass  # MQTT not essential for HTTP honeypot

if __name__ == '__main__':
    print("🚀 HTTP Honeypot starting on port 80...")
    print("📡 Waiting for web attackers...")
    app.run(host='0.0.0.0', port=80, debug=False)
