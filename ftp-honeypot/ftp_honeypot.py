#!/usr/bin/env python3
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
import time
import json
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class HoneypotFTPHandler(FTPHandler):
    def on_connect(self):
        attack_data = {
            'type': 'ftp_connect',
            'ip': self.remote_ip[0],
            'timestamp': time.time(),
            'event': 'connection_attempt'
        }
        self.log_attack(attack_data)
        print(f"🚨 FTP Connection from: {self.remote_ip[0]}")

    def on_login(self, username, password):
        attack_data = {
            'type': 'ftp_login',
            'ip': self.remote_ip[0],
            'username': username,
            'password': password,
            'timestamp': time.time(),
            'event': 'login_attempt'
        }
        self.log_attack(attack_data)
        print(f"🚨 FTP Login attempt: {username}:{password} from {self.remote_ip[0]}")
        return True  # Always accept login to keep them engaged

    def log_attack(self, attack_data):
        try:
            with open('/app/ftp_attacks.json', 'a') as f:
                f.write(json.dumps(attack_data) + '\n')
        except Exception as e:
            print(f"Error logging attack: {e}")

def main():
    # Create authorizer with fake users
    authorizer = DummyAuthorizer()
    authorizer.add_user("admin", "password", "/tmp", perm="elradfmw")
    authorizer.add_user("ftp", "ftp", "/tmp", perm="elradfmw")
    authorizer.add_user("test", "test", "/tmp", perm="elradfmw")
    authorizer.add_anonymous("/tmp")

    # Create handler
    handler = HoneypotFTPHandler
    handler.authorizer = authorizer
    handler.banner = "Welcome to Company FTP Server"

    # Create server
    server = FTPServer(("0.0.0.0", 21), handler)
    
    print("🚀 FTP Honeypot starting on port 21...")
    print("📡 Waiting for FTP attackers...")
    
    server.serve_forever()

if __name__ == '__main__':
    main()
