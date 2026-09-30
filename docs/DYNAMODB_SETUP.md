# TravelGo: DynamoDB Database Setup Guide

> **Epic 3**: DynamoDB Setup — Tasks 6 & 7

---

## Task 6: Navigate to DynamoDB in AWS Console

1. Sign in at **https://console.aws.amazon.com/**
2. In the search bar, type **DynamoDB** and press Enter
3. In the top-right region selector, confirm you are in **Asia Pacific (Mumbai) ap-south-1**
4. Click **Get Started** or **Tables** in the left sidebar

---

## Task 7: Create DynamoDB Tables

TravelGo uses **two tables** to store user credentials and booking records.

### Option A: Automated (Recommended) — Run setup_dynamodb.py

```bash
# From your local machine (with AWS credentials configured) or on EC2
cd TravelGo-App
source venv/bin/activate  # Windows: .\venv\Scripts\Activate
python setup_dynamodb.py
```

The script auto-creates both tables with the correct schema and waits until they are `ACTIVE`.

---

### Option B: Manual via AWS Console

#### Table 1: TravelGo_Users

| Setting | Value |
|---|---|
| Table name | `TravelGo_Users` |
| Partition key | `email` (String) |
| Sort key | *(none)* |
| Table class | DynamoDB Standard |
| Read/Write capacity | **On-demand** (PAY_PER_REQUEST) |

**Steps:**
1. DynamoDB Console → **Create table**
2. Table name: `TravelGo_Users`
3. Partition key: `email` → Type: **String**
4. Leave Sort key blank
5. Table settings: **Customize settings** → Capacity mode: **On-demand**
6. Click **Create table**

---

#### Table 2: TravelGo_Bookings (with GSI)

| Setting | Value |
|---|---|
| Table name | `TravelGo_Bookings` |
| Partition key | `booking_id` (String) |
| Sort key | *(none)* |
| Global Secondary Index | `UserBookingsIndex` |
| GSI Partition key | `user_email` (String) |
| GSI Sort key | `created_at` (String) |
| Billing mode | On-demand (PAY_PER_REQUEST) |

**Steps:**
1. DynamoDB Console → **Create table**
2. Table name: `TravelGo_Bookings`
3. Partition key: `booking_id` → Type: **String**
4. **Additional settings** → **Global Secondary Indexes** → **Create index**:
   - Index name: `UserBookingsIndex`
   - Partition key: `user_email` → **String**
   - Sort key: `created_at` → **String**
   - Projected attributes: **All**
5. Billing: **On-demand**
6. Click **Create table**

---

## Verify Tables in Console

After creation (takes ~30 seconds):
- Both tables show `Active` status in DynamoDB → Tables
- Click `TravelGo_Bookings` → **Indexes** tab → confirm `UserBookingsIndex` is `Active`
