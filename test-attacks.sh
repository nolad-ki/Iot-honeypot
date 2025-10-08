#!/bin/bash
echo "🎯 TESTING ALL HONEYPOTS"
echo "========================"

echo "1. Testing SSH Honeypot..."
sshpass -p "password123" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 2222 testuser@localhost 2>/dev/null
sshpass -p "admin" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 2222 admin@localhost 2>/dev/null
echo "✅ SSH attacks sent"

echo "2. Testing HTTP Honeypot..."
curl -s http://localhost > /dev/null && echo "✅ Homepage accessed"
curl -s http://localhost/admin > /dev/null && echo "✅ Admin page probed"
curl -s "http://localhost/search?q=' OR '1'='1" > /dev/null && echo "✅ SQL injection attempted"
curl -s http://localhost/wp-admin > /dev/null && echo "✅ WordPress admin probed"
curl -s http://localhost/phpmyadmin > /dev/null && echo "✅ phpMyAdmin probed"

echo "3. Testing FTP Honeypot..."
for user in admin root; do
    for pass in password admin; do
        ftp -n localhost << ENDFTP 2>/dev/null
user $user $pass
quit
ENDFTP
    done
done
echo "✅ FTP attacks sent"

echo ""
echo "🎉 All honeypot tests completed!"
