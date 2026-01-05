#!/bin/bash
set -e

echo "🚢 Nigeria Customs Container Scanner → ECR Deploy (eu-west-2)"

# 1. FIXED Requirements (Docker ARM64)
cat > requirements.txt << REQUIREMENTS
opencv-python-headless==4.10.0.84
easyocr==1.7.1
numpy==1.26.4
flask==3.0.3
gunicorn==22.0.0
REQUIREMENTS

# 2. FIXED Dockerfile (eu-west-2)
cat > Dockerfile << DOCKERFILE
FROM python:3.13-slim-bookworm

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libgomp1 libatlas-base-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY src/ ./src/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.dashboard:app"]
DOCKERFILE

# 3. AWS ECR Login (eu-west-2)
echo "Configuring AWS ECR (eu-west-2)..."
aws configure set aws_access_key_id AKIASOYKZNXEZQWXUO5E
aws configure set aws_secret_access_key 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
aws configure set default.region eu-west-2

aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 169136975305.dkr.ecr.eu-west-2.amazonaws.com

# 4. Build + Tag + Push
echo "Building Nigeria Customs Scanner..."
docker build -t ncs-scanner:latest .
docker tag ncs-scanner:latest 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:latest
docker tag ncs-scanner:latest 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:v2.0

echo "🚀 Pushing to ECR..."
docker push 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:latest
docker push 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:v2.0

# 5. Verify
echo "✅ SUCCESS! Production URLs:"
echo "🐳 169136975305.dkr.ecr.eu-west-2.amazonaws.com/container_ai:latest"
echo "📱 Test: docker run -p 8080:8080 [URL]"
echo "🚢 NCS Apapa Port DEPLOYMENT READY!"
