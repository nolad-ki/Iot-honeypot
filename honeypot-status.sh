#!/bin/bash
echo "🔍 Honeypot Security System - Quick Status"
echo "=========================================="

# Find the dashboard port
DASHBOARD_PORT=$(ps aux | grep -o "Local:.*http://localhost:[0-9]*" | grep -o "[0-9]*" | head -1)
if [ -z "$DASHBOARD_PORT" ]; then
    DASHBOARD_PORT="3003"  # Default to the one we know is running
fi

echo "🌐 Dashboard: http://localhost:$DASHBOARD_PORT"
echo "🔧 API: http://localhost:5000"
echo ""

# Honeypot status
echo "📊 Active Honeypots:"
docker ps --filter "name=honeypot" --format "{{.Names}}" | while read honeypot; do
    status=$(docker inspect --format='{{.State.Status}}' $honeypot 2>/dev/null)
    if [ "$status" = "running" ]; then
        echo "   ✅ $honeypot"
    else
        echo "   ❌ $honeypot"
    fi
done

echo ""
echo "🚀 Quick Start:"
echo "   1. Open http://localhost:$DASHBOARD_PORT"
echo "   2. Login with any credentials"
echo "   3. Monitor real-time attacks"
