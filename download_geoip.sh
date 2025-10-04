#!/bin/bash
echo "📥 Downloading GeoIP2 databases..."

# Create directory
mkdir -p geoip-data

# Download free GeoLite2 databases from MaxMind
# Note: You might need to create a free account at https://www.maxmind.com/
# and get a license key for automated downloads

echo "🔍 If you have a MaxMind license key, enter it now (or press Enter to use demo mode):"
read -r LICENSE_KEY

if [ -n "$LICENSE_KEY" ]; then
    echo "📦 Downloading GeoLite2 databases with your key..."
    wget -O geoip-data/GeoLite2-City.mmdb.gz "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=$LICENSE_KEY&suffix=tar.gz"
    wget -O geoip-data/GeoLite2-ASN.mmdb.gz "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-ASN&license_key=$LICENSE_KEY&suffix=tar.gz"
    
    # Extract
    gunzip geoip-data/GeoLite2-City.mmdb.gz
    gunzip geoip-data/GeoLite2-ASN.mmdb.gz
    
    echo "✅ GeoIP databases downloaded and extracted"
else
    echo "🔄 Using demo mode with sample data..."
    # We'll create a simple local database for common IP ranges
    cat > geoip-data/sample_geoip.json << 'EOF'
{
    "8.8.8.8": {"country": "United States", "city": "Mountain View", "isp": "Google LLC", "country_code": "US"},
    "1.1.1.1": {"country": "United States", "city": "Los Angeles", "isp": "Cloudflare", "country_code": "US"},
    "185.165.190.100": {"country": "Russia", "city": "Moscow", "isp": "Unknown", "country_code": "RU"},
    "45.95.147.200": {"country": "Netherlands", "city": "Amsterdam", "isp": "Unknown", "country_code": "NL"},
    "192.168.1.100": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"},
    "10.0.0.1": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"},
    "172.16.0.1": {"country": "Private", "city": "Local Network", "isp": "Internal", "country_code": "LOCAL"}
}
EOF
    echo "✅ Sample GeoIP database created"
fi
