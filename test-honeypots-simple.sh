#!/bin/bash
echo "🎯 SIMPLE HONEYPOT TEST"
echo "======================"

echo "1. Testing HTTP Honeypot (port 80)..."
curl -s http://localhost > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ HTTP: WORKING"
    echo "   Recent logs:"
    docker logs http-honeypot --tail 2 2>/dev/null | head -2
else
    echo "❌ HTTP: NOT WORKING"
fi

echo ""
echo "2. Testing FTP Honeypot (port 21)..."
timeout 3 ftp -n localhost << FTP_TEST 2>/dev/null
user admin admin
quit
FTP_TEST

if [ $? -eq 0 ]; then
    echo "✅ FTP: WORKING"
    echo "   Recent logs:"
    docker logs ftp-honeypot --tail 2 2>/dev/null | head -2
else
    echo "❌ FTP: NOT WORKING"
fi

echo ""
echo "3. Testing SSH Honeypot (port 2222)..."
timeout 3 ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 2222 test@localhost 2>&1 | head -1
echo "✅ SSH: Connection attempted (check logs below)"

echo ""
echo "4. Testing RDP Honeypot (port 3389)..."
python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('localhost',3389)); print('✅ RDP: Connection successful'); s.close()" 2>/dev/null || echo "❌ RDP: Connection failed"

echo ""
echo "5. Testing MySQL Honeypot (port 3306)..."
python3 -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('localhost',3306)); print('✅ MySQL: Connection successful'); s.close()" 2>/dev/null || echo "❌ MySQL: Connection failed"

echo ""
echo "📊 ALL SERVICE LOGS:"
echo "==================="
for service in http-honeypot ftp-honeypot ssh-honeypot rdp-honeypot mysql-honeypot; do
    echo ""
    echo "--- $service ---"
    docker logs $service --tail 3 2>/dev/null | head -3
done
