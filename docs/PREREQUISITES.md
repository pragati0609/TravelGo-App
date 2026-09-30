# TravelGo: Prerequisites & Reference Guide

> **Epic**: Pre-requisites  
> **Task 2**: Pre-requisites  
> **SkillWallet Course**: AWS Cloud Practitioner

---

## 1. Required Services & Official Documentation

Before deploying and running TravelGo, the following AWS services, developer tools, and official documentations are referenced and utilized throughout the project:

| Service / Tool | Purpose in TravelGo | Official Documentation Link | Status |
|---|---|---|:---:|
| **AWS Account Setup** | Root account creation, free-tier activation, and initial console access. | [Getting Started with AWS Accounts](https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html) | Ready |
| **AWS IAM (Identity and Access Management)** | Creating programmatic IAM users, access keys, and the `TravelGo-EC2-Role` instance profile. | [AWS IAM Introduction](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) | Configured |
| **AWS EC2 (Elastic Compute Cloud)** | Launching Ubuntu/AL2023 instances, configuring Security Groups, and hosting the Flask app. | [Amazon EC2 Concepts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html) | Scripted (`deploy.sh`) |
| **AWS DynamoDB** | Managed NoSQL database storing `TravelGo_Users` and `TravelGo_Bookings` tables with GSI. | [Amazon DynamoDB Introduction](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html) | Scripted (`setup_dynamodb.py`) |
| **Amazon SNS (Simple Notification Service)** | Real-time email notifications for confirmed and cancelled bookings via `BookingConfirmation` topic. | [Amazon SNS Welcome Guide](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) | Scripted (`setup_sns.py`) |
| **Git Documentation** | Version control for pushing the codebase to GitHub and cloning onto the EC2 host. | [Official Git Documentation](https://git-scm.com/doc) | Verified & Committed |
| **Visual Studio Code Installation** | Code editing, debugging, and terminal execution environment. | [VS Code Download & Setup](https://code.visualstudio.com/download) | Installed |

---

## 2. Local Environment Requirements

### Installed Runtimes & Tools:
- **Operating System**: Windows 10/11 (or Linux on EC2)
- **Python**: Python 3.9+ (Active: Python 3.13)
- **Version Control**: Git (installed and configured)
- **Editor**: Visual Studio Code (or any IDE)
- **Package Manager**: `pip`

---

## 3. Python Dependencies & Virtual Environment

All necessary Python packages are pinned in [`requirements.txt`](../requirements.txt):

```text
Flask>=3.0.0
boto3>=1.34.0
python-dotenv>=1.0.0
gunicorn>=21.2.0
pytest>=8.0.0
werkzeug>=3.0.0
```

### Installation Steps:
```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

```bash
# Linux / EC2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 4. Configuration Template (.env)

The environment variables are managed through [`.env.example`](../.env.example):
```bash
cp .env.example .env
```
Contains:
- `AWS_REGION=ap-south-1`
- `DYNAMODB_USERS_TABLE=TravelGo_Users`
- `DYNAMODB_BOOKINGS_TABLE=TravelGo_Bookings`
- `SNS_TOPIC_ARN=...`
- `SECRET_KEY=...`
