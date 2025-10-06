#!/bin/bash
echo "🎯 SIMULATING ATTACKS ON ALL HONEYPOTS"
echo "====================================="

echo "1. 🕵️‍♂️ Testing SSH Honeypot (Cowrie)..."
for i in {1..3}; do
    echo "   Attempt $i: Testing common credentials"
    sshpass -p "password$i" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 2222 user$i@localhost 2>/dev/null
    sshpass -p "admin" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 -p 2222 admin@localhost 2>/dev/null
    sleep 1
done

echo "2. 🌐 Testing HTTP Honeypot..."
curl -s http://localhost > /dev/null
curl -s http://localhost/admin > /dev/null
curl -s "http://localhost/search?q=' OR '1'='1" > /dev/null
curl -s http://localhost/wp-admin > /dev/null
curl -s http://localhost/phpmyadmin > /dev/null

echo "3. 📁 Testing FTP Honeypot..."
# Create FTP commands in a file first
cat > /tmp/ftp_commands.txt << FTPEOF
user admin admin
quit
FTPEOF

cat > /tmp/ftp_test.sh << 'FTPEOF'
#!/bin/bash
for user in admin root test ftp guest; do
    for pass in password admin 123456 test secret; do
        echo "Testing: $user/$pass"
        ftp -n localhost << ENDFTP
user $user $pass
quit
ENDFTP
    done
    sleep 0.5
done
FTPEOF

chmod +x /tmp/ftp_test.sh
/timeout 10 /tmp/ftp_test.sh

echo "✅ All attack simulations completed!"
