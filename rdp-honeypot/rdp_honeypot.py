#!/usr/bin/env python3
import socket
import threading
import time
import json
import struct

class RDPHoneypot:
    def __init__(self, host='0.0.0.0', port=3389):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def log_attack(self, attack_data):
        try:
            with open('/app/rdp_attacks.json', 'a') as f:
                f.write(json.dumps(attack_data) + '\n')
            print(f"📝 RDP Attack logged: {attack_data['type']} from {attack_data['ip']}")
        except Exception as e:
            print(f"Logging error: {e}")

    def handle_client(self, client_socket, client_ip):
        print(f"🚨 RDP Connection from: {client_ip}")
        
        # Log connection attempt
        self.log_attack({
            'timestamp': time.time(),
            'type': 'rdp_connect',
            'ip': client_ip,
            'event': 'connection_attempt'
        })
        
        try:
            # Send RDP negotiation response
            response = b'\x03\x00\x00\x13\x0e\xd0\x00\x00\x12\x34\x00\x02\x00\x08\x00\x02\x00\x00\x00'
            client_socket.send(response)
            
            # Try to read more data (credentials attempt)
            client_socket.settimeout(5.0)
            data = client_socket.recv(1024)
            
            if data:
                print(f"🔍 RDP Data received from {client_ip}: {data[:50]}...")
                self.log_attack({
                    'timestamp': time.time(),
                    'type': 'rdp_data',
                    'ip': client_ip,
                    'data_hex': data.hex()[:100],
                    'event': 'data_received'
                })
                
        except socket.timeout:
            print(f"⏰ RDP Timeout from {client_ip}")
        except Exception as e:
            print(f"❌ RDP Error with {client_ip}: {e}")
        finally:
            client_socket.close()
            print(f"🔒 RDP Connection closed: {client_ip}")

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print(f"🚀 RDP Honeypot started on {self.host}:{self.port}")
            print("🖥️  Waiting for Windows RDP attackers...")
            
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
            print(f"❌ RDP Server error: {e}")
        finally:
            self.socket.close()

if __name__ == '__main__':
    honeypot = RDPHoneypot()
    honeypot.start()
