# TravelGo: SNS Notification Setup Guide

> **Epic 4**: SNS Setup — Tasks 8 & 9

---

## Task 8: Create an SNS Topic Named `BookingConfirmation`

Amazon SNS (Simple Notification Service) delivers real-time email notifications every time a user books or cancels a trip.

### Option A: Automated — Run setup_sns.py

```bash
# Replace with your email address
python setup_sns.py your-email@example.com
```

The script:
1. Creates the `BookingConfirmation` SNS topic
2. Subscribes your email to it
3. Prints the `SNS_TOPIC_ARN` you need to paste into `.env`

---

### Option B: Manual via AWS Console

#### Create the Topic

1. Open **SNS → Topics → Create topic**
2. **Type**: Standard (not FIFO — we need fanout to email subscribers)
3. **Name**: `BookingConfirmation`
4. **Display name**: `TravelGo`
5. Leave all other settings as default
6. Click **Create topic**
7. **Copy the Topic ARN** — it looks like: `arn:aws:sns:ap-south-1:123456789012:BookingConfirmation`

---

## Task 9: Subscribe Your Email Endpoint to the Topic

#### Subscribe Email (Console)

1. On the `BookingConfirmation` topic page → **Subscriptions** tab → **Create subscription**
2. **Protocol**: Email
3. **Endpoint**: Enter your email address (e.g. `your-email@example.com`)
4. Click **Create subscription**

#### Confirm Subscription

1. Open your email inbox — look for:
   - **From**: `no-reply@sns.amazonaws.com`
   - **Subject**: `AWS Notification - Subscription Confirmation`
2. Click **Confirm subscription** link in the email
3. Back in AWS Console → Subscription status changes to **Confirmed** ✅

---

## Update Your .env File

After creating the topic, paste the ARN into your `.env`:

```env
SNS_TOPIC_ARN=arn:aws:sns:ap-south-1:YOUR_ACCOUNT_ID:BookingConfirmation
```

---

## How TravelGo Uses SNS

| Event | SNS Message Sent |
|---|---|
| Booking confirmed | Subject: `TravelGo: Booking Confirmed (BK-XXXXXXXX)` |
| Booking cancelled | Subject: `TravelGo: Booking Cancelled (BK-XXXXXXXX)` |

The `aws_service.send_sns_notification()` method (in [`services/aws_service.py`](../services/aws_service.py)) publishes the message automatically at the end of every `create_booking()` and `cancel_booking()` call.
