#!/usr/bin/env python3
import socket
import threading
import paramiko
import time
import json
import sys

class SimpleSSHHoneypot(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.log_attack({
            'timestamp': time.time(),
            'type': 'ssh_connect',
            'ip': client_ip,
            'event': 'connection_attempt'
        })
        print(f"🚨 SSH Connection from: {client_ip}")

    def check_auth_password(self, username, password):
        print(f"🔑 SSH Login attempt: {username}:{password} from {self.client_ip}")
        self.log_attack({
            'timestamp': time.time(),
            'type': 'ssh_login',
            'ip': self.client_ip,
            'username': username,
            'password': password,
            'event': 'login_attempt'
        })
        return paramiko.AUTH_FAILED  # Always fail auth

    def log_attack(self, data):
        try:
            with open('/app/ssh_attacks.json', 'a') as f:
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            print(f"Log error: {e}")

def handle_ssh_connection(client_socket, client_ip):
    try:
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey.generate(2048))
        
        honeypot = SimpleSSHHoneypot(client_ip)
        transport.start_server(server=honeypot)
        
        # Keep connection open for a bit
        time.sleep(5)
        transport.close()
        
    except Exception as e:
        print(f"SSH error with {client_ip}: {e}")
    finally:
        client_socket.close()
        print(f"🔒 SSH Connection closed: {client_ip}")

def start_ssh_honeypot():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', 2222))
        server_socket.listen(5)
        print("🚀 Simple SSH Honeypot started on port 2222")
        print("🔐 Waiting for SSH attackers...")
        
        while True:
            client_socket, client_addr = server_socket.accept()
            client_ip = client_addr[0]
            
            client_thread = threading.Thread(
                target=handle_ssh_connection,
                args=(client_socket, client_ip)
            )
            client_thread.daemon = True
            client_thread.start()
            
    except Exception as e:
        print(f"❌ SSH Server error: {e}")
    finally:
        server_socket.close()

if __name__ == '__main__':
    start_ssh_honeypot()
