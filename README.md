# TravelGo 🌐✈️

> **A Cloud-Powered Real-Time Travel Booking Platform Using AWS**  
> *SkillWallet — AWS Cloud Practitioner Project*

---

## 🚀 Project Overview

TravelGo is a full-stack, cloud-based travel booking platform that allows users to:
- **Register & Log In** with secure hashed credentials stored in Amazon DynamoDB
- **Search & Book** Buses (interactive seat selection), Trains, Flights, and Hotels in one unified interface
- **Receive instant email notifications** via Amazon SNS when bookings are confirmed or cancelled
- **Manage travel history** through a dynamic personal dashboard with real-time status and one-click cancellation

---

## 🏛️ Technical Architecture

| Component | AWS Service | Purpose |
|---|---|---|
| Web Application Backend | **Amazon EC2** (Flask + Gunicorn) | Hosts the booking platform with auto-restart |
| User & Booking Data | **Amazon DynamoDB** | NoSQL, millisecond-latency key-value storage |
| Real-Time Email Alerts | **Amazon SNS** | Instant `BookingConfirmation` topic notifications |
| Security & Permissions | **AWS IAM** | EC2 Instance Role — no hardcoded credentials |
| Monitoring | **Amazon CloudWatch** | Application logs and health metrics |

---

## 📋 Project Epics & Tasks (All 18 Completed)

See [`docs/CONCLUSION.md`](docs/CONCLUSION.md) for the full task completion summary.

---

## 🛠️ Local Setup & Running

### Prerequisites
- Python 3.9+
- AWS Account with IAM credentials (or EC2 Instance Profile)

### Quick Start
```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/TravelGo-App.git
cd TravelGo-App

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: .\venv\Scripts\Activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env: set AWS_REGION and SNS_TOPIC_ARN

# 5. (Optional) Provision DynamoDB tables
python setup_dynamodb.py

# 6. (Optional) Create SNS topic and subscribe
python setup_sns.py your-email@example.com

# 7. Run the application
python app.py
```

Open your browser at **http://localhost:5000**

---

## ☁️ AWS Deployment on EC2

```bash
# SSH into your EC2 instance
ssh -i travelgo-key.pem ubuntu@YOUR_EC2_PUBLIC_IP

# Upload and run the automated deploy script
chmod +x deploy.sh
./deploy.sh
```

See [`docs/EC2_SETUP.md`](docs/EC2_SETUP.md) for detailed EC2 setup, security group configuration, and IAM role setup.

---

## 📚 Documentation Index

| Document | Description |
|---|---|
| [`docs/ER_DIAGRAM.md`](docs/ER_DIAGRAM.md) | Entity Relationship Diagram & DynamoDB Schema |
| [`docs/PREREQUISITES.md`](docs/PREREQUISITES.md) | System & software prerequisites |
| [`docs/PROJECT_FLOW.md`](docs/PROJECT_FLOW.md) | End-to-end sequence diagrams (3 Scenarios) |
| [`docs/IAM_SETUP.md`](docs/IAM_SETUP.md) | IAM Role creation and policy attachment |
| [`docs/EC2_SETUP.md`](docs/EC2_SETUP.md) | EC2 launch, security groups, and deployment |
| [`docs/TESTING.md`](docs/TESTING.md) | Functional test checklist and verification |
| [`docs/CONCLUSION.md`](docs/CONCLUSION.md) | Final architecture review and skills demonstrated |

---

## 🔔 Key AWS Services Configured

- **DynamoDB Tables**: `TravelGo_Users`, `TravelGo_Bookings`
- **DynamoDB GSI**: `UserBookingsIndex` (for instant user dashboard queries)
- **SNS Topic**: `BookingConfirmation` (for real-time email alerts)
- **IAM Role**: `TravelGo-EC2-Role` (attached to EC2 instance)
- **EC2 Security Group**: Ports 22 (SSH), 80 (HTTP), 5000 (Flask)

---

## 👩‍💻 Developer

**Pragati Trivedi**  
AWS Cloud Practitioner — SkillWallet  
Mentor: Midhun Kotagiri (midhun+mentor@thesmartbridge.com)
