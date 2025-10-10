#!/usr/bin/env python3
import socket
import threading
import time
from datetime import datetime
import sqlite3

# Import our database module
import honeypot_db

print("🎯 REAL-TIME HONEYPOT CAPTURE SERVICE STARTED...")

# Simple TCP capture for SSH-like services
def capture_ssh_like(port, service_name):
    def handle_connection(client_sock, addr):
        try:
            client_sock.send(b"Welcome to SSH Service\r\nlogin: ")
            data = client_sock.recv(1024)
            username = data.decode().strip()
            
            client_sock.send(b"password: ")
            data = client_sock.recv(1024)
            password = data.decode().strip()
            
            honeypot_db.log_attack(service_name, addr[0], username, password, "login attempt")
            client_sock.send(b"Access denied\r\n")
        except:
            pass
        finally:
            client_sock.close()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"✅ {service_name.upper()} capture on port {port}")
    
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client, addr)).start()

# Start capture services
threading.Thread(target=capture_ssh_like, args=(22224, "ssh_simple"), daemon=True).start()
threading.Thread(target=capture_ssh_like, args=(23234, "telnet_simple"), daemon=True).start()

print("🚀 Ready! Test on ports 22224 (SSH-like) and 23234 (Telnet-like)")
print("💡 These will capture directly to database!")

# Keep running
while True:
    time.sleep(1)
