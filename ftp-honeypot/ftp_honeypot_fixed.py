#!/usr/bin/env python3
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
import time
import json
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class FixedFTPHoneypot(FTPHandler):
    def on_connect(self):
        client_ip = self.remote_ip
        print(f"🚨 FTP CONNECTION from {client_ip}")
        self.log_attack({
            'timestamp': time.time(),
            'type': 'ftp_connect',
            'ip': client_ip,
            'event': 'connection_attempt'
        })

    def on_login(self, username, password):
        client_ip = self.remote_ip
        print(f"🚨 FTP LOGIN: {username}:{password} from {client_ip}")
        self.log_attack({
            'timestamp': time.time(),
            'type': 'ftp_login',
            'ip': client_ip,
            'username': username,
            'password': password,
            'event': 'login_attempt'
        })
        return True

    def log_attack(self, data):
        try:
            with open('/app/ftp_attacks.json', 'a') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            print(f"Log error: {e}")

def main():
    print("🚀 Starting Fixed FTP Honeypot...")
    
    authorizer = DummyAuthorizer()
    authorizer.add_user("admin", "admin", "/tmp", perm="elradfmw")
    authorizer.add_user("ftp", "ftp", "/tmp", perm="elradfmw") 
    authorizer.add_user("test", "test", "/tmp", perm="elradfmw")
    authorizer.add_user("root", "password", "/tmp", perm="elradfmw")
    authorizer.add_anonymous("/tmp")

    handler = FixedFTPHoneypot
    handler.authorizer = authorizer
    handler.banner = "220 Welcome to Corporate FTP Server"
    
    server = FTPServer(("0.0.0.0", 21), handler)
    print("📡 FTP Honeypot ready! Waiting for attackers...")
    
    server.serve_forever()

if __name__ == '__main__':
    main()
