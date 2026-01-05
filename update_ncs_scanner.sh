#!/bin/bash
set -e

echo "🚢 NCS Scanner Auto-Deploy → ECR (eu-west-2)"

VERSION_FILE="VERSION"
if [ -f "$VERSION_FILE" ]; then
    CURRENT_VERSION=$(cat $VERSION_FILE)
    NEXT_VERSION=$(echo $CURRENT_VERSION | awk -F. '{ $NF+=1; OFS="." }1')
else
    NEXT_VERSION="v2.1"
fi

echo "📦 Building version: $NEXT_VERSION"
echo $NEXT_VERSION > $VERSION_FILE
git add $VERSION_FILE
git commit -m "📦 v$NEXT_VERSION" || true

cat > Dockerfile << 'DOCKERFILE'
FROM python:3.13-slim-bookworm
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 wget \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY src/ ./src/
RUN pip install --only-binary=all \
    flask==3.0.3 gunicorn==22.0.0 numpy easyocr opencv-python-headless
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.dashboard:app"]
DOCKERFILE

aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 169136975305.dkr.ecr.eu-west-2.amazonaws.com

docker build -t ncs-scanner:$NEXT_VERSION .
docker tag ncs-scanner:$NEXT_VERSION 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:$NEXT_VERSION
docker tag ncs-scanner:$NEXT_VERSION 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:latest

echo "🚀 Pushing v$NEXT_VERSION..."
docker push 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:$NEXT_VERSION
docker push 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:latest

echo "✅ DEPLOY COMPLETE v$NEXT_VERSION!"
echo "🐳 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:$NEXT_VERSION"
