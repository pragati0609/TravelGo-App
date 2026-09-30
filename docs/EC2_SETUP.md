# TravelGo: EC2 Instance Setup Guide

> **Epic 6**: EC2 Instance Setup — Tasks 12, 13, 14

---

## Task 13: Launch an EC2 Instance to Host the Flask App

### AWS Management Console Steps

1. Go to **EC2 → Instances → Launch Instances**
2. **Name**: `TravelGo-Server`
3. **AMI (OS Image)**: `Ubuntu 22.04 LTS (HVM)` — Free Tier Eligible, or Amazon Linux 2023
4. **Instance Type**: `t2.micro` (Free Tier) or `t3.micro` for slightly better performance
5. **Key Pair**: Create a new `.pem` key pair → `travelgo-key.pem`
   - **Save it securely** — you cannot download it again
6. **IAM Instance Profile**: Attach `TravelGo-EC2-Role` (created in Epic 5)
7. **Storage**: Default 8 GB gp3 SSD is sufficient

---

## Task 14: Configure Security Groups

### Security Group Name: `TravelGo-SG`

| Rule | Protocol | Port | Source | Purpose |
|---|---|---|---|---|
| SSH | TCP | **22** | `0.0.0.0/0` (or restrict to your IP) | Remote terminal access |
| HTTP | TCP | **80** | `0.0.0.0/0` | Public web access (Nginx proxy) |
| HTTPS | TCP | **443** | `0.0.0.0/0` | Secure web access (optional) |
| Custom TCP | TCP | **5000** | `0.0.0.0/0` | Direct Flask app access (testing) |

> **Tip**: For production, restrict port 5000 to only allow internal traffic and serve publicly via Nginx on port 80.

---

## Connect to Your EC2 Instance

```bash
# From Windows PowerShell or Linux/macOS Terminal
# Replace 'ec2-54-123-456-789.compute.amazonaws.com' with your actual EC2 DNS/IP

# Make PEM file not publicly readable (Linux/macOS only)
chmod 400 travelgo-key.pem

# SSH in
ssh -i travelgo-key.pem ubuntu@ec2-54-123-456-789.compute.amazonaws.com
# For Amazon Linux 2023, user is 'ec2-user'
ssh -i travelgo-key.pem ec2-user@ec2-54-123-456-789.compute.amazonaws.com
```

---

## Task 12: Push Project Files to GitHub (Do this FIRST from your local PC)

```bash
# From your local machine inside C:\My Projects\TravelGo\TravelGo-App
git init
git add .
git commit -m "Initial commit: TravelGo AWS Cloud Platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/TravelGo-App.git
git push -u origin main
```

---

## Task 15: Install Software on the EC2 Instance

```bash
# Once connected via SSH, run the deployment script
chmod +x deploy.sh
./deploy.sh
```

Or manually step-by-step:
```bash
# 1. System packages
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv git nginx

# 2. Create app directory
mkdir -p ~/TravelGo-App && cd ~/TravelGo-App

# 3. Create virtualenv
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

---

## Task 16: Clone and Run the Flask App

```bash
# Clone from GitHub
git clone https://github.com/YOUR_USERNAME/TravelGo-App.git ~/TravelGo-App
cd ~/TravelGo-App

# Create and configure .env
cp .env.example .env
nano .env   # Set AWS_REGION and SNS_TOPIC_ARN

# Provision DynamoDB tables
source venv/bin/activate
python setup_dynamodb.py

# Start Flask with Gunicorn (production-grade WSGI server)
gunicorn --bind 0.0.0.0:5000 --workers 3 app:app
```

### Test the live application:
```
http://YOUR_EC2_PUBLIC_IP:5000
```
