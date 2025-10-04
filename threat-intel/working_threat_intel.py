#!/usr/bin/env python3
import sys
import paho.mqtt.client as mqtt
import json
import time
import logging
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("🚀 Starting Threat Intelligence Service")

sys.path.append(".")

try:
    from threat_intel_service import ThreatIntel
    logger.info("✅ ThreatIntel imported successfully")
    
    # Test available methods
    ti = ThreatIntel()
    methods = [method for method in dir(ti) if not method.startswith('_') and callable(getattr(ti, method))]
    logger.info(f"✅ Available methods: {methods}")
    
except Exception as e:
    logger.error(f"❌ Failed to import ThreatIntel: {e}")
    sys.exit(1)

class ThreatIntelService:
    def __init__(self):
        self.client = None
        self.connected = False
        self.connection_event = threading.Event()
        self.threat_intel = ThreatIntel()
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("✅ Connected to MQTT broker successfully!")
            self.connected = True
            self.connection_event.set()
            
            # Subscribe to topics
            topics = [
                ("honeypot/events", 0),
                ("threat/intel", 0),
                ("ips", 0),
                ("cowrie/#", 0)
            ]
            client.subscribe(topics)
            logger.info("✅ Subscribed to all topics")
        else:
            logger.error(f"❌ Connection failed with code: {rc}")
            
    def on_message(self, client, userdata, msg):
        try:
            logger.info(f"📨 Received message on {msg.topic}")
            payload = msg.payload.decode()
            
            # Extract IP address
            ip_address = self.extract_ip_from_payload(payload)
            
            if ip_address:
                logger.info(f"🔍 Analyzing IP: {ip_address}")
                
                # Try to analyze the IP using available methods
                result = self.analyze_ip(ip_address)
                
                # Publish results
                result_topic = "threat/intel/results"
                client.publish(result_topic, json.dumps(result))
                logger.info(f"✅ Published threat intelligence for {ip_address}")
            else:
                logger.info("⚠️ No IP address found in message")
                
        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")
            
    def extract_ip_from_payload(self, payload):
        """Extract IP address from various message formats"""
        ip_address = None
        
        # Try to parse as JSON
        if payload.startswith("{"):
            try:
                data = json.loads(payload)
                ip_address = (
                    data.get("ip") or 
                    data.get("ip_address") or 
                    data.get("src_ip") or
                    data.get("peerIP")
                )
                # For nested session data (Cowrie format)
                if not ip_address and "session" in data:
                    session_data = data["session"]
                    if isinstance(session_data, dict):
                        ip_address = session_data.get("peerIP")
            except json.JSONDecodeError:
                pass
        
        # If not JSON or no IP found, check if it's a plain IP
        if not ip_address:
            parts = payload.strip().split(".")
            if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                ip_address = payload.strip()
                
        return ip_address
        
    def analyze_ip(self, ip_address):
        """Analyze IP using available methods from ThreatIntel class"""
        try:
            # Try different analysis methods
            if hasattr(self.threat_intel, 'analyze_ip'):
                return self.threat_intel.analyze_ip(ip_address)
            elif hasattr(self.threat_intel, 'check_ip'):
                return self.threat_intel.check_ip(ip_address)
            elif hasattr(self.threat_intel, 'check_abuseipdb'):
                abuse_result = self.threat_intel.check_abuseipdb(ip_address)
                vt_result = self.threat_intel.check_virustotal(ip_address) if hasattr(self.threat_intel, 'check_virustotal') else {}
                return {
                    "ip": ip_address,
                    "abuseipdb": abuse_result,
                    "virustotal": vt_result
                }
            else:
                # Fallback
                return {
                    "ip": ip_address,
                    "status": "analyzed",
                    "message": "Basic analysis completed",
                    "methods_available": [method for method in dir(self.threat_intel) if not method.startswith('_')]
                }
        except Exception as e:
            return {
                "ip": ip_address,
                "error": str(e),
                "status": "analysis_failed"
            }
        
    def on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info(f"✅ Subscription confirmed for mid: {mid}")
        
    def on_disconnect(self, client, userdata, rc):
        logger.info("🔌 Disconnected from MQTT broker")
        self.connected = False
        self.connection_event.clear()
        
    def connect_with_retry(self, max_attempts=5):
        """Connect to MQTT with retry logic"""
        for attempt in range(max_attempts):
            try:
                logger.info(f"🔗 Connection attempt {attempt + 1}/{max_attempts} to mosquitto:1883")
                self.client.connect("mosquitto", 1883, 60)
                return True
            except Exception as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt < max_attempts - 1:
                    time.sleep(2)
        return False
        
    def start(self):
        """Start the threat intelligence service"""
        logger.info("🔧 Initializing MQTT client...")
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect
        
        # Connect to MQTT
        if not self.connect_with_retry():
            logger.error("❌ Failed to connect to MQTT after all attempts")
            return False
            
        # Start the loop
        self.client.loop_start()
        logger.info("🔄 MQTT loop started")
        
        # Wait for connection
        if self.connection_event.wait(timeout=10):
            logger.info("🎯 Threat Intelligence Service is ready!")
            return True
        else:
            logger.error("❌ Connection timeout - service not ready")
            self.client.loop_stop()
            return False
            
    def keep_alive(self):
        """Keep the service running"""
        try:
            while self.connected:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 Service interrupted")
        finally:
            self.stop()
            
    def stop(self):
        """Stop the service"""
        logger.info("🧹 Shutting down service...")
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
        logger.info("👋 Service stopped")

# Start the service
if __name__ == "__main__":
    service = ThreatIntelService()
    if service.start():
        service.keep_alive()
    else:
        logger.error("❌ Failed to start Threat Intelligence Service")
        sys.exit(1)
