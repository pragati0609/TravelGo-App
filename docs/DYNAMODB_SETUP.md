# TravelGo: DynamoDB Database Creation and Setup Guide

> **Epic 3**: DynamoDB Database Creation and Setup — Tasks 6 & 7  
> **SkillWallet Course**: AWS Cloud Practitioner

---

## Task 6: Navigate to DynamoDB

1. Log in to the **[AWS Management Console](https://aws.amazon.com/console/)** (or via Troven temporary lab credentials).
2. Ensure your active AWS region is **Asia Pacific (Mumbai) `ap-south-1`** (top-right header).
3. In the top search bar, type **DynamoDB** and press Enter.
4. On the DynamoDB Dashboard, click the orange **"Create table"** button (or navigate to **Tables** in the left sidebar and click **Create table**).

---

## Task 7: Create DynamoDB Tables for Storing Registration Details and Booking Records

TravelGo uses **two dedicated DynamoDB tables**:
1. **`travel-Users`**: Stores registered user accounts and authentication credentials.
2. **`Bookings`**: Stores travel and lodging reservations across buses, trains, flights, and hotels.

---

### Step 1: Create the `travel-Users` Table

| Setting | Value | Description |
|---|---|---|
| **Table name** | `travel-Users` | Table for storing user registration and login data |
| **Partition key** | `Email` | Type: **String** |
| **Sort key** | *(Leave blank)* | Single-attribute primary key |
| **Table settings** | **Default settings** (or On-Demand) | Free-tier / Pay per request |

**Detailed Console Steps:**
1. In the **Table details** section:
   - **Table name**: Enter `travel-Users`
   - **Partition key**: Enter `Email` and select **String** from the dropdown
2. Leave the **Sort key** field blank.
3. Under **Table settings**, select **Default settings** (or choose **Customize settings** &rarr; **On-demand** capacity mode).
4. Click the orange **"Create table"** button at the bottom of the page.
5. Wait ~15 seconds until the status shows as **Active** ✅.

---

### Step 2: Create the `Bookings` Table

| Setting | Value | Description |
|---|---|---|
| **Table name** | `Bookings` | Table for storing travel & accommodation records |
| **Partition key** | `email` | Type: **String** |
| **Sort key** | `booking_id` | Type: **String** |
| **Table settings** | **Default settings** (or On-Demand) | Composite primary key |

**Detailed Console Steps:**
1. Return to the Tables list and click **"Create table"** again.
2. In the **Table details** section:
   - **Table name**: Enter `Bookings`
   - **Partition key**: Enter `email` and select **String**
   - **Sort key**: Enter `booking_id` and select **String**
3. Under **Table settings**, choose **Default settings** (or **On-demand** capacity).
4. Click **"Create table"**.
5. Wait until the status changes to **Active** ✅.

---

## Automated Creation (Optional Script)

You can also run the pre-configured automation script to create both tables in your account:

```bash
# From TravelGo-App directory:
python setup_dynamodb.py
```

This will automatically create `travel-Users` (Partition Key: `Email`) and `Bookings` (Partition Key: `email`, Sort Key: `booking_id`).

---

## Verification Checklist

In the AWS Console under **DynamoDB &rarr; Tables**, verify:
- [x] `travel-Users` status is **Active** with Partition key `Email (String)`.
- [x] `Bookings` status is **Active** with Partition key `email (String)` and Sort key `booking_id (String)`.
