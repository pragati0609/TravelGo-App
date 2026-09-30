#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# TravelGo EC2 Deployment Script
# Task 15-16: Install software on EC2 and run the Flask application
#
# Run this script on a fresh EC2 instance (Amazon Linux 2023 / Ubuntu 22.04)
# after SSHing in and cloning the repository from GitHub.
#
# Usage:
#   chmod +x deploy.sh
#   ./deploy.sh
# ─────────────────────────────────────────────────────────────────────────────

set -e  # Exit immediately on any error

APP_DIR="$HOME/TravelGo-App"
SERVICE_NAME="travelgo"
APP_PORT=5000

echo "======================================================"
echo "  TravelGo Cloud Platform — EC2 Deployment"
echo "======================================================"

# ─── Step 1: System Update & Python Installation ──────────────────────────────
echo ""
echo "[1/6] Updating system packages..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip python3-venv git nginx
elif command -v yum &> /dev/null; then
    sudo yum update -y
    sudo yum install -y python3 python3-pip git nginx
fi
echo "[OK] System packages installed."

# ─── Step 2: Clone / Pull from GitHub ─────────────────────────────────────────
echo ""
echo "[2/6] Setting up application directory..."
if [ -d "$APP_DIR" ]; then
    echo "Directory exists. Pulling latest changes..."
    cd "$APP_DIR" && git pull
else
    echo "Cloning repository from GitHub..."
    # REPLACE with your actual GitHub repository URL
    git clone https://github.com/YOUR_USERNAME/TravelGo-App.git "$APP_DIR"
fi
cd "$APP_DIR"
echo "[OK] Repository is up to date."

# ─── Step 3: Python Virtual Environment & Dependencies ───────────────────────
echo ""
echo "[3/6] Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
echo "[OK] Python dependencies installed."

# ─── Step 4: Environment Configuration ────────────────────────────────────────
echo ""
echo "[4/6] Configuring environment variables..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "IMPORTANT: Please edit .env to add your SNS_TOPIC_ARN."
    echo "           On EC2 with IAM role, leave AWS credentials empty."
fi
echo "[OK] Environment configured."

# ─── Step 5: Create DynamoDB Tables ───────────────────────────────────────────
echo ""
echo "[5/6] Provisioning DynamoDB tables..."
source venv/bin/activate
python setup_dynamodb.py || echo "Tables may already exist — continuing."

# ─── Step 6: Create Systemd Service for Auto-Restart ─────────────────────────
echo ""
echo "[6/6] Creating systemd service for auto-start on boot..."
VENV_PYTHON="$APP_DIR/venv/bin/python"
GUNICORN="$APP_DIR/venv/bin/gunicorn"

sudo bash -c "cat > /etc/systemd/system/${SERVICE_NAME}.service <<EOF
[Unit]
Description=TravelGo Flask Application (Gunicorn)
After=network.target

[Service]
User=$USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$GUNICORN --bind 0.0.0.0:${APP_PORT} --workers 3 --timeout 120 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

echo ""
echo "======================================================"
echo "  Deployment Complete!"
echo "======================================================"
echo ""
echo "  Service Status : sudo systemctl status $SERVICE_NAME"
echo "  App URL        : http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || echo 'YOUR_EC2_PUBLIC_IP'):${APP_PORT}"
echo "  App Logs       : sudo journalctl -u $SERVICE_NAME -f"
echo ""
