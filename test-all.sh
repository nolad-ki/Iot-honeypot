#!/bin/bash
echo "🎯 TESTING ALL HONEYPOTS"
echo "========================"

echo "1. Testing SSH Honeypot (2222)..."
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 2222 test@localhost 2>/dev/null && echo "✅ SSH test sent" || echo "❌ SSH test failed"

echo "2. Testing HTTP Honeypot (80)..."
curl -s --max-time 3 http://localhost > /dev/null && echo "✅ HTTP test sent" || echo "❌ HTTP test failed"

echo "3. Testing FTP Honeypot (21)..."
timeout 3 ftp -n localhost << EOF 2>/dev/null
user test test
quit
