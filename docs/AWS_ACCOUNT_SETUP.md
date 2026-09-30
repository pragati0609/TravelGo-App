# TravelGo: AWS Account Setup Guide

> **Epic 2**: AWS Account Setup — Task 5

---

## Task 5: AWS Account Setup and Login

### Step 1: Create or Login to Your AWS Account

1. Visit **https://console.aws.amazon.com/**
2. If you don't have an account, click **Create a new AWS account**
   - Enter your email, set a root password
   - Add billing info (a valid credit/debit card — Free Tier will not charge you)
   - Verify phone number
   - Select **Free Tier** plan
3. Sign in to the **AWS Management Console**

---

### Step 2: Create an IAM User with Programmatic Access

> **Best Practice**: Never use your root account credentials for application access.

1. Open **IAM → Users → Create user**
2. **User name**: `travelgo-developer`
3. **Permission**: Attach policies directly → select:
   - `AmazonDynamoDBFullAccess`
   - `AmazonSNSFullAccess`
4. Click **Create user**
5. Open the user → **Security credentials** tab → **Create access key**
6. **Use case**: `Application running outside AWS`
7. **Download the `.csv` file** — you will NOT be able to view the secret key again

---

### Step 3: Configure AWS CLI

```bash
# Install AWS CLI (if not already installed)
# Windows: Download MSI from https://aws.amazon.com/cli/
# Linux/Mac: pip install awscli

aws configure
# AWS Access Key ID: AKIA...
# AWS Secret Access Key: xxxxx
# Default region name: ap-south-1
# Default output format: json
```

### Verify Configuration:
```bash
aws sts get-caller-identity
# Should return your account ID and user ARN
```

---

### Step 4: Set AWS Region to Mumbai (ap-south-1)

All TravelGo resources are created in **ap-south-1 (Mumbai)** for lowest latency from India.

In your `.env` file:
```env
AWS_REGION=ap-south-1
```
