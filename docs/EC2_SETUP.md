# TravelGo: EC2 Instance Setup Guide

> **Epic 6**: EC2 Instance Setup — Tasks 12, 13, 14  
> **SkillWallet Course**: AWS Cloud Practitioner

---

## Task 12: Load Your Project Files to GitHub

All Flask backend application code, templates, static assets, DynamoDB/SNS provisioning scripts, and documentation inside `TravelGo-App` are prepared and committed to Git locally.

### Command to push to your GitHub repository:
From your local terminal on your machine:
```powershell
cd "C:\My Projects\TravelGo\TravelGo-App"
git push origin main
```
Your repository is accessible at:
> **https://github.com/pragati0609/TravelGo-App**

---

## Task 13: Launch an EC2 Instance to Host the Flask App

### Step-by-Step Console Walkthrough:
1. Sign in to the **AWS Management Console** and navigate to the **EC2 Dashboard**.
2. Click the orange **"Launch instance"** button.
3. **Name and tags**: Enter `TravelGo-Server`.
4. **Application and OS Images (Amazon Machine Image)**:
   - Select **Amazon Linux 2** or **Ubuntu Server 22.04 LTS** (both are Free tier eligible).
5. **Instance type**:
   - Choose **`t2.micro`** (Free tier eligible: 1 vCPU, 1 GiB Memory).
6. **Key pair (login)**:
   - Click **Create new key pair**.
   - Key pair name: `travelgo-key`
   - Key pair type: **RSA**
   - Private key file format: **`.pem`**
   - Click **Create key pair** and save the downloaded file securely.
7. Click **Launch instance** at the bottom right.

---

## Task 14: Configure Security Groups for HTTP and SSH Access

### Inbound Firewall Rules:
During launch (or under **EC2 &rarr; Security Groups &rarr; Edit inbound rules**), configure the following:

| Type | Protocol | Port Range | Source | Purpose |
|---|---|---|---|---|
| **SSH** | TCP | `22` | `0.0.0.0/0` (or My IP) | Remote shell access & EC2 Instance Connect |
| **HTTP** | TCP | `80` | `0.0.0.0/0` (Anywhere) | Public web access to Flask / Nginx |
| **Custom TCP** | TCP | `5000` | `0.0.0.0/0` (Anywhere) | Direct Flask development port access |

---

## Connecting via EC2 Instance Connect (Browser-Based Terminal)

To access your server directly from your browser without third-party software:

### Step 1: Attach the IAM Role
1. In the **EC2 Console &rarr; Instances**, select your `TravelGo-Server` instance.
2. Click **Actions &rarr; Security &rarr; Modify IAM role**.
3. Select **`TravelGo-EC2-Role`** (created in Epic 5) from the dropdown list.
4. Click **Update IAM role** ✅.

### Step 2: Open EC2 Instance Connect
1. With your instance selected, click the **Connect** button at the top of the EC2 Dashboard.
2. Under connection methods, select the **EC2 Instance Connect** tab.
3. Verify the username (`ubuntu` for Ubuntu, or `ec2-user` for Amazon Linux).
4. Click the orange **"Connect"** button.
5. A new browser window/tab will open with a full Linux shell terminal!

---

---

## Task 15: Install Software on the EC2 Instance

Once connected to your EC2 via **EC2 Instance Connect** (browser terminal), run the following commands **one by one**:

```bash
# Update package list
sudo apt update

# Install Python pip
sudo apt install python3-pip -y

# Install Git
sudo apt install git -y

# Install Python virtual environment module
sudo apt install python3-venv -y

# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

---

## Task 16: Clone Your Flask Project from GitHub and Run the App

```bash
# Clone your project repository from GitHub
git clone https://github.com/pragati0609/TravelGo-App.git

# Navigate into the project directory
cd TravelGo-App

# Set the SNS Topic ARN as an environment variable
export SNS_TOPIC_ARN=arn:aws:sns:ap-south-1:557690616836:BookingConfirmation

# Install Flask and Boto3
pip install flask boto3

# Run the Flask application (with sudo to bind to port 80)
sudo -E venv/bin/python3 app.py
```

> **Note**: `sudo -E` preserves the environment variables (like `SNS_TOPIC_ARN`) when running as root. This is required to bind the Flask app to port 80.

Once the app is running, open your browser and navigate to your **EC2 Public IP**:
```
http://<YOUR_EC2_PUBLIC_IP>/
```
You should see the TravelGo homepage live on AWS! 🎉
