# TravelGo: AWS IAM Role Setup Guide

> **Epic 5**: IAM Role Setup — Tasks 10 & 11  
> **SkillWallet Course**: AWS Cloud Practitioner

---

## Task 10: Create IAM Role

An **IAM Role** allows your Amazon EC2 instance to securely communicate with DynamoDB and SNS without saving permanent secret access keys in the code or environment files.

### Step-by-Step Console Walkthrough:
1. Log in to the **[AWS Management Console](https://aws.amazon.com/console/)**.
2. In the top search bar, type **IAM** and select **IAM (Identity and Access Management)**.
3. In the left navigation menu, click **Roles**, then click the blue **"Create role"** button.
4. **Step 1 - Select trusted entity**:
   - **Trusted entity type**: Select **AWS service**.
   - **Use case**: Select **EC2** (Allows EC2 instances to call AWS services on your behalf).
   - Click **Next**.

---

## Task 11: Attach Policies

### Attach the Required AWS Managed Policies:

On the **Add permissions** page, search for and check the following two policies:

| Policy Name | Description & Purpose |
|---|---|
| **`AmazonDynamoDBFullAccess`** | Allows EC2 to perform read/write operations on DynamoDB (`travel-Users` and `Bookings` tables). |
| **`AmazonSNSFullAccess`** | Grants EC2 the ability to send notifications via SNS (publish to `BookingConfirmation` topic). |

### Finalize Role Creation:
1. Search for `AmazonDynamoDBFullAccess` in the filter box and check the box next to it.
2. Clear the search, then search for `AmazonSNSFullAccess` and check the box next to it.
3. Click **Next**.
4. **Role details**:
   - **Role name**: Enter `TravelGo-EC2-Role` (or `travelgo-ec2-role`)
   - **Description**: `Allows TravelGo EC2 Flask application to access DynamoDB and SNS without hardcoded credentials.`
5. Click **"Create role"** at the bottom right.
6. A green banner will confirm: *Role `TravelGo-EC2-Role` created.* ✅

---

## Attaching the Role to Your EC2 Instance (Used in Epic 6 & 7)

When launching or managing your EC2 instance:
1. Open the **Amazon EC2 Console &rarr; Instances**.
2. Select your `TravelGo-Server` instance.
3. Click **Actions &rarr; Security &rarr; Modify IAM role**.
4. Select `TravelGo-EC2-Role` from the dropdown.
5. Click **Update IAM role**.

### Verification from EC2:
Once attached, Boto3 inside Flask automatically retrieves temporary credentials via IMDSv2:
```bash
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
```
No `AWS_ACCESS_KEY_ID` or `AWS_SECRET_ACCESS_KEY` needs to be saved in `.env`!
