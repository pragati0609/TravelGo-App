# TravelGo: Prerequisites & Environment Setup Guide

> **Epic**: Pre-requisites  
> **Task 2**: Pre-requisites

---

## 1. System Requirements Verification

- **Operating System**: Windows 10/11, Ubuntu 20.04+, macOS Monterey+
- **Python**: Python 3.9+ (Installed: Python 3.13)
- **Framework**: Flask 3.x
- **Cloud SDK**: AWS CLI v2 & Boto3

---

## 2. Virtual Environment Setup

### On Windows:
```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### On Linux (Ubuntu / EC2 Amazon Linux):
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Environment Configuration

Copy the template configuration file:
```bash
cp .env.example .env
```
Fill in your designated AWS Region (e.g. `ap-south-1` or `us-east-1`), DynamoDB table names, and SNS topic ARN.

When deployed to an EC2 instance with an attached IAM Role, **no hardcoded credentials** are needed—Boto3 resolves temporary security tokens automatically through instance metadata (`IMDSv2`).
