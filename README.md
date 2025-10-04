# 🐝 IoT Honeypot System

A comprehensive, Docker-based honeypot system designed to capture, analyze, and monitor cyber attacks in real-time. 
This system emulates IoT devices and services to attract attackers while providing detailed threat intelligence.

![Honeypot Architecture](https://img.shields.io/badge/Architecture-Docker--Compose-blue)
![Status](https://img.shields.io/badge/Status-Operational-green)
![Security](https://img.shields.io/badge/Security-Honeypot-orange)

## 🏗️ System Architecture
📦 Iot-honeypot/
├── 🐳 docker-compose.yml              # Main orchestration
├── 🐛 cowrie/                         # SSH/Telnet Honeypot
├── 🤖 threat-intel/                   # Threat Intelligence Engine
├── 📡 mosquitto/                      # MQTT Message Broker
├── 📊 telemetry/                      # IoT Device Simulator
├── 👥 fake-subscriber/                # MQTT Message Consumer
├── 🔧 device-api/                     # Device Management API
├── 📈 log-enrichment/                 # Log Processing
├── 🌐 geoip-data/                     # Geolocation Database
└── 📁 cowrie-data/                    # Attack Logs (local)

## 🚀 Quick Start
## Prerequisites
- Docker & Docker Compose
- Git
- 2GB RAM minimum

### Deployment
# Clone the repository
git clone git@github.com:nolad-ki/Iot-honeypot.git
cd Iot-honeypot

# Start all services
docker-compose up -d

# Monitor attacks in real-time
docker logs -f cowrie

### Verification

# Check all services are running
docker-compose ps

# Test SSH honeypot
ssh -p 2222 root@localhost

# Test Telnet honeypot  
telnet localhost 2223

## 📊 Services Overview

### 1. 🐛 Cowrie Honeypot
**Ports**: 2222 (SSH), 2223 (Telnet)  
**Purpose**: Emulates SSH and Telnet services to capture authentication attempts and shell interactions.

**Features**:
- Realistic SSH banner emulation
- Interactive shell environment
- Command execution logging
- File download monitoring
- Session recording

**Captures**:
- Brute force attacks
- Command execution attempts
- Malware downloads
- Credential stuffing

### 2. 🤖 Threat Intelligence Service
**Purpose**: Analyzes attacker IP addresses and provides real-time threat assessment.

**Analysis Methods**:
- IP reputation scoring
- Geographic attribution
- Historical attack patterns
- Real-time threat level calculation

**Output**:
- Threat scores (0-100)
- Country of origin
- Attack frequency
- Risk assessment

### 3. 📡 MQTT Messaging Infrastructure
**Ports**: 1883 (MQTT), 9001 (WebSocket)  
**Purpose**: Real-time message bus for inter-service communication.

**Topics**:
- `honeypot/events` - General attack events
- `threat/intel` - Threat intelligence requests
- `threat/intel/results` - Analysis results
- `cowrie/#` - Cowrie-specific events
- `devices/+/telemetry` - IoT device data

### 4. 📊 Telemetry Service
**Purpose**: Generates fake IoT device data to simulate real IoT environments.

**Simulated Devices**:
- Smart thermostats
- Security cameras
- Environmental sensors
- Smart locks

**Data Types**:
- Temperature readings
- Humidity levels
- Device status
- Motion detection

### 5. 👥 Fake Subscriber
**Purpose**: Consumes MQTT messages for processing and analysis.

## 🔧 Configuration

### Environment Variables
Create `.env` file:

# Threat Intelligence APIs (optional)
ABUSEIPDB_API_KEY=your_abuseipdb_key
VIRUSTOTAL_API_KEY=your_virustotal_key

# MQTT Configuration
MQTT_HOST=mosquitto
MQTT_PORT=1883

# Honeypot Settings
COWRIE_SSH_PORT=2222
COWRIE_TELNET_PORT=2223

### Docker Compose Services
yaml
services:
  cowrie:
    build: ./cowrie
    ports: ["2222:2222", "23:2223"]
    networks: [honeypot-net]
    
  threat-intel:
    build: ./threat-intel
    environment: [MQTT_HOST=mosquitto, MQTT_PORT=1883]
    networks: [honeypot-net]
    
  mosquitto:
    image: eclipse-mosquitto:latest
    ports: ["1883:1883", "9001:9001"]
    networks: [honeypot-net]

## 📈 Monitoring & Analysis

### Real-time Monitoring

# Live attack feed
docker logs -f cowrie

# Threat analysis results
docker logs -f threat-intel

# MQTT message traffic
docker exec -it mosquitto mosquitto_sub -h localhost -t "#" -v

# System resource usage
docker stats

### Log Analysis

# Recent attacks (last hour)
docker logs cowrie --since 1h | grep -E "(login attempt|connection)"

# Threat intelligence summary
docker logs threat-intel --since 24h | grep -E "(Analyzing|Threat score)"

# Error monitoring
docker-compose logs --tail=50 | grep -i error


### Data Export

# Export Cowrie logs
docker exec cowrie cat /cowrie-data/cowrie.json > attacks.json

# Export threat intelligence data
docker logs threat-intel > threat_analysis.log


## 🛡️ Security Features

### Attack Detection
- **Authentication Monitoring**: Failed login attempts
- **Command Analysis**: Suspicious command execution
- **Network Scanning**: Port scanning detection
- **Malware Capture**: File download monitoring

### Threat Intelligence
- **IP Reputation**: Real-time threat scoring
- **Behavioral Analysis**: Attack pattern recognition
- **Geolocation**: Attacker origin mapping
- **Historical Tracking**: Repeat offender identification

### Data Protection
- **Container Isolation**: Services run in isolated containers
- **Network Segmentation**: Internal Docker network
- **Log Encryption**: Secure log storage
- **Access Control**: Limited exposed ports

## 🔄 Management Commands

### Service Management

# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# Restart specific service
docker-compose restart cowrie

# View service status
docker-compose ps

# View service logs
docker-compose logs [service]


### Maintenance

# Update services
docker-compose pull
docker-compose up -d

# Clean up Docker
docker system prune -f

# Backup data
tar -czf honeypot-backup-$(date +%Y%m%d).tar.gz cowrie-data/

# Update from GitHub
git pull origin main
docker-compose up -d --build

### Troubleshooting

# Check service health
docker-compose logs --tail=20

# Test MQTT connectivity
docker exec threat-intel python -c "import socket; s=socket.socket(); s.settimeout(2); print('MQTT:', 'OK' if s.connect_ex(('mosquitto',1883))==0 else 'FAIL')"

# Verify ports are open
nc -zv localhost 2222
nc -zv localhost 2223

# Check resource usage
docker stats --no-stream


## 📊 Performance Metrics

### Resource Requirements
- **CPU**: 2+ cores recommended
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 10GB+ for log storage
- **Network**: Minimal bandwidth required

### Expected Load
- **Concurrent Connections**: 50-100
- **Log Generation**: 10-100MB/day
- **Attack Volume**: Varies by deployment

## 🚨 Security Considerations

### ⚠️ Important Warnings
1. **Isolated Deployment**: Always deploy in isolated environment
2. **Network Segmentation**: Use separate VLAN/VPC
3. **Legal Compliance**: Ensure honeypot usage complies with local laws
4. **Data Privacy**: Do not capture sensitive information
5. **Monitoring**: Continuously monitor honeypot activity

### Best Practices
- Deploy behind firewall with limited ingress
- Use non-routable IP addresses
- Regular security updates
- Monitor for compromise
- Regular log analysis

## 🤝 Contributing

### Development Setup

# Fork repository
git clone git@github.com:nolad-ki/Iot-honeypot.git
cd Iot-honeypot

# Create feature branch
git checkout -b feature/new-detection-method

# Test changes
docker-compose up -d --build
docker-compose logs -f

# Submit pull request
git push origin feature/new-detection-method

### Areas for Contribution
- New detection methods
- Additional honeypot services
- Enhanced threat intelligence
- Improved logging
- Performance optimization

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Cowrie Project**: SSH/Telnet honeypot foundation
- **Eclipse Mosquitto**: MQTT broker implementation
- **Docker Community**: Containerization platform
- **Security Researchers**: Threat intelligence methodologies



### Documentation
- [Cowrie Documentation](https://cowrie.readthedocs.io/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [MQTT Protocol](https://mqtt.org/)

### Issues
Report issues and feature requests on [GitHub Issues](https://github.com/nolad-ki/Iot-honeypot/issues)

### Community
Join discussions and share findings with the cybersecurity community.



**Maintained by**: [nolad-ki](https://github.com/nolad-ki)  
**Last Updated**:
**System Status**: 🟢 OPERATIONAL

> **Warning**: This is a honeypot system designed to attract attackers. Use responsibly and in compliance with applicable laws.
EOF

# Add and commit the comprehensive README
git add README.md
git commit -m "docs: Add comprehensive README with complete system documentation"
git push


This README now includes:

## 📋 **Complete Documentation:**
- **System Architecture** with all components
- **Quick Start** deployment instructions
- **Service Details** for each component
- **Configuration** guides
- **Monitoring** and analysis procedures
- **Security** considerations and warnings
- **Management** commands and troubleshooting
- **Performance** metrics and requirements
- **Contributing** guidelines
- **License** and acknowledgments

## 🎯 **Key Features Documented:**
- Real-time attack monitoring
- Threat intelligence analysis
- MQTT messaging infrastructure
- IoT device simulation
- Docker containerization
- Security best practices
- Maintenance procedures

