#!/bin/bash
set -e

echo "📱 NCS Scanner → ECR Deploy (eu-west-2)"

echo "🔐 Logging into ECR..."
aws ecr get-login-password --region eu-west-2 | \
  docker login --username AWS --password-stdin \
  169136975305.dkr.ecr.eu-west-2.amazonaws.com || {
  echo "❌ AWS CLI/ECR login failed. Check IAM keys!"
  exit 1
}

# Stop old container
docker stop ncs-scanner 2>/dev/null || true
docker rm ncs-scanner 2>/dev/null || true

echo "⬇️ Pulling latest ECR image..."
docker pull 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:latest

mkdir -p data

echo "🚀 Deploying NCS Scanner..."
docker run -d --name ncs-scanner \
  --restart=always \
  -p 8080:8080 \
  -v $(pwd)/data:/app/data \
  169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:latest

sleep 5
echo "✅ DEPLOY COMPLETE!"
echo "📱 http://localhost:8080"
echo "📊 Data: $(pwd)/data/"
docker ps | grep ncs-scanner
curl -s localhost:8080 | head -20 || echo "⏳ Starting..."
