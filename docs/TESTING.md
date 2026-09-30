# TravelGo: Testing & Validation Guide

> **Epic 8**: Testing and Deployment — Task 17

---

## Functional Test Checklist

### 1. User Authentication Tests

| Test Case | Action | Expected Result |
|---|---|---|
| Register new user | POST `/auth/register` with valid form | Redirects to Login with success flash |
| Duplicate email | Register again with same email | Shows "Email already registered" error |
| Login valid | POST `/auth/login` | Redirects to Dashboard, session created |
| Login invalid password | POST `/auth/login` wrong password | Shows "Invalid email or password" |
| Logout | GET `/auth/logout` | Session cleared, redirected to Home |

### 2. Multi-Mode Booking Tests (Scenario 1)

| Test Case | Action | Expected Result |
|---|---|---|
| Search buses | GET `/search?mode=bus&origin=Hyderabad` | Returns bus listings |
| Search trains | GET `/search?mode=train` | Returns train listings |
| Search flights | GET `/search?mode=flight` | Returns flight listings |
| Search hotels | GET `/search?mode=hotel&category=luxury` | Filters luxury hotels only |
| Select bus seats | GET `/select-seats/BUS-01` | Interactive seat matrix visible |
| Book bus | Select seats → Confirm | Creates booking, redirects to confirmation |
| Instant book (train/flight/hotel) | Click Book Now | Creates booking, redirects to confirmation |

### 3. SNS Real-Time Notification Tests (Scenario 2)

| Test Case | Expected Result |
|---|---|
| Booking confirmed | SNS `BookingConfirmation` topic publishes an email |
| Email received | Inbox has subject: "TravelGo: Booking Confirmed (BK-XXXXXXXX)" |
| Cancellation | SNS publishes "TravelGo: Booking Cancelled (BK-XXXXXXXX)" |
| `sns_message_id` stored | `TravelGo_Bookings` table has `sns_message_id` attribute set |

### 4. Dynamic Dashboard Tests (Scenario 3)

| Test Case | Action | Expected Result |
|---|---|---|
| View all bookings | GET `/dashboard` | All user bookings listed, stats shown |
| Filter by mode | GET `/dashboard?tab=bus` | Only bus bookings shown |
| Cancel booking | POST `/cancel-booking/<id>` | Status changes to CANCELLED in DynamoDB |
| DynamoDB record check | AWS Console → DynamoDB → Explore items | Item `booking_status = CANCELLED` |

---

## Running the Automated Tests

```bash
# From TravelGo-App directory with venv active
python -m pytest tests/ -v --tb=short
```

---

## Manual DynamoDB Verification

1. Open **AWS Console → DynamoDB → Tables**
2. Click `TravelGo_Bookings` → **Explore table items**
3. Confirm booking records have all fields: `booking_id`, `user_email`, `booking_status`, `sns_message_id`

## CloudWatch Logs Verification

```bash
# On EC2 instance
sudo journalctl -u travelgo -f --no-pager
```
