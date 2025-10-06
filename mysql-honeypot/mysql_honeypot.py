#!/usr/bin/env python3
import socket
import threading
import time
import json
import struct

class MySQLHoneypot:
    def __init__(self, host='0.0.0.0', port=3306):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def log_attack(self, attack_data):
        try:
            with open('/app/mysql_attacks.json', 'a') as f:
                f.write(json.dumps(attack_data) + '\n')
            print(f"📝 MySQL Attack logged: {attack_data['type']} from {attack_data['ip']}")
        except Exception as e:
            print(f"Logging error: {e}")

    def send_handshake(self, client_socket):
        # MySQL initial handshake packet
        handshake = (
            b'\x4a\x00\x00\x00\x0a' +  # Protocol version 10
            b'8.0.25' + b'\x00' +       # Server version
            b'\x00' * 18 +              # Connection ID
            b'\x00' * 8 +               # Auth plugin data part 1
            b'\x00' +                   # Filler
            b'\xff\xf7' +               # Capability flags
            b'\x21' +                   # Character set
            b'\x02\x00' +               # Status flags
            b'\xff\x81' +               # Extended capabilities
            b'\x15' +                   # Auth plugin data len
            b'\x00' * 10 +              # Reserved
            b'\x00' * 13 +              # Auth plugin data part 2
            b'mysql_native_password' + b'\x00'  # Auth plugin name
        )
        client_socket.send(handshake)

    def parse_login(self, data, client_ip):
        try:
            # Basic attempt to extract username from login packet
            if len(data) > 36:
                username_end = data[36:].find(b'\x00')
                if username_end != -1:
                    username = data[36:36+username_end].decode('utf-8', errors='ignore')
                    print(f"🔑 MySQL Login attempt from {client_ip}: username={username}")
                    
                    self.log_attack({
                        'timestamp': time.time(),
                        'type': 'mysql_login',
                        'ip': client_ip,
                        'username': username,
                        'event': 'login_attempt'
                    })
                    return username
        except Exception as e:
            print(f"Error parsing MySQL login: {e}")
        
        print(f"🔑 MySQL Connection from {client_ip} (could not parse credentials)")
        self.log_attack({
            'timestamp': time.time(),
            'type': 'mysql_connect',
            'ip': client_ip,
            'event': 'connection_attempt'
        })
        return "unknown"

    def handle_client(self, client_socket, client_ip):
        print(f"🚨 MySQL Connection from: {client_ip}")
        
        try:
            # Send MySQL handshake
            self.send_handshake(client_socket)
            
            # Receive login attempt
            client_socket.settimeout(10.0)
            data = client_socket.recv(4096)
            
            if data:
                username = self.parse_login(data, client_ip)
                
                # Send error response (access denied)
                error_response = (
                    b'\x17\x00\x00\x01\xff' +  # Error packet
                    b'\x48\x04' +              # Error code 1092
                    b'#28000' +                # SQL state
                    b'Access denied for user ' + username.encode() + b'\'@\'' + client_ip.encode() + b'\''
                )
                client_socket.send(error_response)
                
        except socket.timeout:
            print(f"⏰ MySQL Timeout from {client_ip}")
        except Exception as e:
            print(f"❌ MySQL Error with {client_ip}: {e}")
        finally:
            client_socket.close()
            print(f"🔒 MySQL Connection closed: {client_ip}")

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"🚀 MySQL Honeypot started on {self.host}:{self.port}")
            print("🗄️  Waiting for database attackers...")
            
            while True:
                client_socket, client_addr = self.socket.accept()
                client_ip = client_addr[0]
                
                # Handle each connection in a new thread
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, client_ip)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"❌ MySQL Server error: {e}")
        finally:
            self.socket.close()

if __name__ == '__main__':
    honeypot = MySQLHoneypot()
    honeypot.start()
