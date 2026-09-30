# TravelGo: End-to-End Project Flow & Architecture Sequences

> **Epic**: Project Flow  
> **Task 3**: Topic Links / Project Flow

---

## 1. System Request & Data Flow Overview

TravelGo orchestrates three primary AWS components around a Python Flask web core:
1. **Amazon EC2**: Hosts the Flask backend service behind a reverse proxy/WSGI server.
2. **Amazon DynamoDB**: Provides millisecond key-value and document persistence for user credentials and booking history.
3. **Amazon SNS (Simple Notification Service)**: Dispatches instant booking and cancellation alerts to subscribers via the `BookingConfirmation` topic.

---

## 2. Sequence Diagram 1: User Registration & Authentication

```mermaid
sequenceDiagram
    autonumber
    actor User as Passenger
    participant UI as Browser / Frontend
    participant App as Flask Backend (EC2)
    participant DDB as DynamoDB (TravelGo_Users)

    Note over User, DDB: Registration Flow
    User->>UI: Fills Register Form (Name, Email, Phone, Password)
    UI->>App: POST /register
    App->>App: Hash password (PBKDF2/SHA256)
    App->>DDB: GetItem(email)
    alt User Already Exists
        DDB-->>App: User Record Found
        App-->>UI: 400 Bad Request ("Email already registered")
    else User is New
        App->>DDB: PutItem(email, user_id, full_name, phone, password_hash, created_at)
        DDB-->>App: 200 OK
        App-->>UI: Redirect to /login with Flash Success
    end

    Note over User, DDB: Login Flow
    User->>UI: Enters Email & Password
    UI->>App: POST /login
    App->>DDB: GetItem(email)
    DDB-->>App: Returns User Item
    App->>App: Verify Password Hash
    alt Credentials Valid
        App->>App: Set session['user_email'] & session['user_name']
        App-->>UI: Redirect /dashboard
    else Invalid Password
        App-->>UI: 401 Unauthorized ("Invalid email or password")
    end
```

---

## 3. Sequence Diagram 2: Multi-Mode Booking & Real-Time SNS Notification (Scenario 1 & 2)

```mermaid
sequenceDiagram
    autonumber
    actor User as Passenger
    participant UI as TravelGo UI
    participant App as Flask Backend (EC2)
    participant DDB as DynamoDB (TravelGo_Bookings)
    participant SNS as Amazon SNS (BookingConfirmation)
    actor Inbox as User / Admin Email

    User->>UI: Selects Travel Mode (e.g., Bus, Train, Flight, Hotel)
    UI->>App: GET /search?mode=bus&from=Hyderabad&to=Bangalore
    App-->>UI: Returns available listings & interactive seat matrix

    User->>UI: Selects Seats (e.g., 12A, 12B) & clicks "Confirm Booking"
    UI->>App: POST /book (mode, origin, destination, seats, price)

    App->>App: Generate Booking ID (BK-XXXX) & timestamp
    App->>DDB: PutItem in TravelGo_Bookings<br/>(booking_id, user_email, mode, origin, destination, seats, total_amount, status='CONFIRMED')
    DDB-->>App: Item Created Successfully

    Note over App, SNS: Scenario 2: Real-time SNS Trigger
    App->>SNS: Publish(TopicArn='BookingConfirmation',<br/>Subject='TravelGo Booking Confirmed',<br/>Message=Booking Details JSON/Text)
    SNS-->>App: MessageId returned
    SNS--)Inbox: Sends instant email confirmation alert
    
    App-->>UI: Redirect /booking-confirmation/<booking_id>
```

---

## 4. Sequence Diagram 3: Travel History Dashboard & Cancellation Workflow (Scenario 3)

```mermaid
sequenceDiagram
    autonumber
    actor User as Passenger
    participant UI as Dashboard UI
    participant App as Flask Backend (EC2)
    participant DDB as DynamoDB (TravelGo_Bookings)
    participant SNS as Amazon SNS (BookingConfirmation)
    actor Inbox as User / Admin Email

    User->>UI: Navigates to /dashboard
    UI->>App: GET /dashboard (Session: user_email)
    App->>DDB: Query(IndexName='UserBookingsIndex',<br/>KeyConditionExpression='user_email = :email')
    DDB-->>App: List of User Bookings (Upcoming & Past)
    App-->>UI: Render Dynamic Dashboard with Categorized Tabs & Cancel Buttons

    User->>UI: Clicks "Cancel Booking" on Booking BK-XXXX
    UI->>App: POST /cancel-booking/<booking_id>
    App->>DDB: UpdateItem(booking_id, status='CANCELLED', cancelled_at=timestamp)
    DDB-->>App: Item Updated

    App->>SNS: Publish(TopicArn='BookingConfirmation',<br/>Subject='TravelGo Booking Cancelled',<br/>Message=Cancellation Details)
    SNS--)Inbox: Sends instant cancellation email alert
    App-->>UI: Redirect /dashboard with Flash "Booking successfully cancelled"
```
