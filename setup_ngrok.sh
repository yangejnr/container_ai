#!/bin/bash
TOKEN="36TSgmyExuGnToz4qveQlLDQ3a6_5CGJ2PwVJ1G6os4hvdjXZ"

echo "🚀 ngrok + NCS Scanner Setup..."

# Install ngrok ARM64
cd /tmp
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
tar xvzf ngrok-v3-stable-linux-arm64.tgz
sudo mv ngrok /usr/local/bin/
rm -rf ngrok*

# Add YOUR token
ngrok config add-authtoken $TOKEN
echo "✅ Token added!"

# Test
ngrok version

echo "🌐 READY! Run: cd ~/container_ai && ngrok http 8080"
