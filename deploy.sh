#!/bin/bash
# ─────────────────────────────────────────────────────────────────────────────
# TravelGo EC2 Deployment Script
# Epic 7 — Tasks 15 & 16: Install Software and Run the Flask Application
#
# Run this script on a fresh EC2 instance (Ubuntu 22.04 LTS)
# inside the EC2 Instance Connect browser terminal.
#
# Usage (run each command one by one as per SkillWallet portal):
#   chmod +x deploy.sh
#   ./deploy.sh
#
# OR run the exact SkillWallet commands manually (see docs/EC2_SETUP.md):
# ─────────────────────────────────────────────────────────────────────────────

# ─── Task 15: Install Software on the EC2 Instance ───────────────────────────
# Step 1: Update and install Python + pip
sudo apt update
sudo apt install python3-pip -y

# Step 2: Install Git
sudo apt install git -y

# Step 3: Install Python virtual environment
sudo apt install python3-venv -y

# Step 4: Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# ─── Task 16: Clone Your Flask Project from GitHub ───────────────────────────
# Step 5: Clone the project repository
git clone https://github.com/pragati0609/TravelGo-App.git

# Step 6: Navigate into the project directory
cd TravelGo-App

# Step 7: Set the SNS Topic ARN environment variable
export SNS_TOPIC_ARN=arn:aws:sns:ap-south-1:557690616836:BookingConfirmation

# Step 8: Install Flask and Boto3
pip install flask boto3

# Step 9: Run the Flask application (requires root for port 80)
sudo -E venv/bin/python3 app.py
