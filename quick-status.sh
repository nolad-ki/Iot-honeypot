#!/bin/bash
echo "🛡️  QUICK HONEYPOT STATUS"
echo "========================"
echo "Last updated: $(date)"
echo ""

echo "📊 RUNNING SERVICES:"
docker-compose ps

echo ""
echo "🌐 PORTS LISTENING:"
for port in 21 80 2222 3389 3306; do
    status=$(nc -zv localhost $port 2>&1 | grep -q "succeeded" && echo "✅" || echo "❌")
    echo "  Port $port: $status"
done

echo ""
echo "🚨 RECENT LOGS:"
services=$(docker-compose ps --services)
for service in $services; do
    echo "$service:"
    docker logs $service --tail 1 2>/dev/null | head -1 || echo "  No logs"
done
