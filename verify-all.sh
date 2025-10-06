#!/bin/bash
echo "🔍 VERIFYING HONEYPOT FLEET"
echo "==========================="

echo "1. Container Status:"
docker-compose ps

echo ""
echo "2. Port Listening Status:"
ports=(21 80 2222 3389 3306)
for port in "${ports[@]}"; do
    if nc -zv localhost $port 2>&1 | grep -q "succeeded"; then
        echo "✅ Port $port: LISTENING"
    else
        echo "❌ Port $port: CLOSED"
    fi
done

echo ""
echo "3. Service Logs (last line):"
services=("http-honeypot" "ftp-honeypot" "rdp-honeypot" "mysql-honeypot" "ssh-honeypot")
for service in "${services[@]}"; do
    echo -n "$service: "
    docker logs $service --tail 1 2>/dev/null | head -1 || echo "No logs"
done

echo ""
echo "4. Quick Connectivity Test:"
echo -n "HTTP: "; curl -s --max-time 2 http://localhost > /dev/null && echo "✅" || echo "❌"
echo -n "FTP:  "; timeout 2 ftp -n localhost < /dev/null > /dev/null 2>&1 && echo "✅" || echo "❌"
echo -n "SSH:  "; timeout 2 ssh -o ConnectTimeout=1 -p 2222 test@localhost > /dev/null 2>&1 && echo "✅" || echo "❌"
