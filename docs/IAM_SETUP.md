# TravelGo: AWS IAM Role Setup Guide

> **Epic 5**: IAM Role Setup — Tasks 10 & 11

---

## Overview

TravelGo's Flask backend on EC2 needs secure, credential-free access to two AWS services:
- **Amazon DynamoDB** – for reading and writing user and booking records
- **Amazon SNS** – for publishing real-time booking notification messages

Instead of hardcoding `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, we attach an **IAM Role** with a scoped policy directly to the EC2 instance. Boto3 automatically fetches short-lived temporary credentials from the instance metadata endpoint (`IMDSv2`).

---

## Task 10: Create the IAM Role

### Step-by-Step (AWS Management Console)

1. Open **IAM → Roles → Create role**
2. **Trusted entity type**: `AWS Service`
3. **Use case**: `EC2`
4. Click **Next**

---

## Task 11: Attach Policies to the IAM Role

### Policies to Attach (Principle of Least Privilege)

| Policy | ARN | Purpose |
|---|---|---|
| `AmazonDynamoDBFullAccess` | `arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess` | Read/Write to `TravelGo_Users` and `TravelGo_Bookings` tables |
| `AmazonSNSFullAccess` | `arn:aws:iam::aws:policy/AmazonSNSFullAccess` | Publish messages to `BookingConfirmation` topic |
| `CloudWatchAgentServerPolicy` | `arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy` | Publish application logs to CloudWatch |

### Steps:
1. On the **Permissions** page, search and check each policy above
2. Click **Next**
3. **Role name**: `TravelGo-EC2-Role`
4. **Description**: `Allows TravelGo EC2 Flask app to access DynamoDB and SNS without hardcoded keys`
5. Click **Create role**

---

## Attach Role to Your EC2 Instance

1. Open **EC2 → Instances → Select your TravelGo instance**
2. Click **Actions → Security → Modify IAM role**
3. Select `TravelGo-EC2-Role` from the dropdown
4. Click **Update IAM role**

### Verify from EC2 Instance:
```bash
# This should return the role name and temporary credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```

---

## Inline Policy (Minimum Privilege Alternative)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:CreateTable",
        "dynamodb:ListTables",
        "dynamodb:DescribeTable"
      ],
      "Resource": [
        "arn:aws:dynamodb:ap-south-1:*:table/TravelGo_Users",
        "arn:aws:dynamodb:ap-south-1:*:table/TravelGo_Bookings",
        "arn:aws:dynamodb:ap-south-1:*:table/TravelGo_Bookings/index/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "sns:Publish",
        "sns:CreateTopic",
        "sns:Subscribe",
        "sns:ListTopics"
      ],
      "Resource": "arn:aws:sns:ap-south-1:*:BookingConfirmation"
    }
  ]
}
```
