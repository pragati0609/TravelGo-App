# TravelGo: End-to-End Project Flow & Architecture Sequences

> **Epic**: Project Flow  
> **Task 3**: Topic Links / Project Flow  
> **SkillWallet Course**: AWS Cloud Practitioner

---

## 1. Project Epic & User Story Roadmap

The project flow structures the implementation of **TravelGo** into 8 sequential Epics, encompassing 13 User Stories and concluding with system testing and verification:

| Epic | User Stories | Deliverable / Implementation | Status |
|---|---|---|:---:|
| **Epic 1: Backend Development and Application Setup** | • Story 1: Develop the Backend Using Flask<br/>• Story 2: Integrate AWS Services Using boto3 | [`app.py`](../app.py), [`routes/`](../routes/), [`services/aws_service.py`](../services/aws_service.py) | ✅ Completed |
| **Epic 2: AWS Account Setup and Login** | • Story 1: Set Up an AWS Account<br/>• Story 2: Log In to the AWS Management Console | [`docs/AWS_ACCOUNT_SETUP.md`](AWS_ACCOUNT_SETUP.md) | ✅ Guide Ready |
| **Epic 3: DynamoDB Database Creation and Setup** | • Story 1: Create a DynamoDB Table<br/>• Story 2: Configure Attributes for User Data and Book Requests | [`setup_dynamodb.py`](../setup_dynamodb.py), [`docs/DYNAMODB_SETUP.md`](DYNAMODB_SETUP.md) | ✅ Completed |
| **Epic 4: SNS Notification Setup** | • Story 1: Create SNS Topics for Book Request Notifications<br/>• Story 2: Subscribe Users to SNS Email Notifications | [`setup_sns.py`](../setup_sns.py), [`docs/SNS_SETUP.md`](SNS_SETUP.md) | ✅ Completed |
| **Epic 5: IAM Role Setup** | • Story 1: Create IAM Role (`TravelGo-EC2-Role`)<br/>• Story 2: Attach Policies (`DynamoDBFullAccess`, `SNSFullAccess`) | [`docs/IAM_SETUP.md`](IAM_SETUP.md) | ✅ Guide Ready |
| **Epic 6: EC2 Instance Setup** | • Story 1: Launch an EC2 Instance (Ubuntu/AL2023)<br/>• Story 2: Configure Security Groups (Ports 22, 80, 5000) | [`docs/EC2_SETUP.md`](EC2_SETUP.md) | ✅ Guide Ready |
| **Epic 7: Deployment on EC2** | • Story 1: Upload Flask Files (via GitHub clone)<br/>• Story 2: Run the Flask Application (Gunicorn + Systemd) | [`deploy.sh`](../deploy.sh), [`docs/EC2_SETUP.md`](EC2_SETUP.md) | ✅ Scripted |
| **Epic 8: Testing and Deployment** | • Story 1: Conduct Functional Testing | [`tests/test_app.py`](../tests/test_app.py) (17/17 passed), [`docs/TESTING.md`](TESTING.md) | ✅ Verified |
| **Conclusion** | • Final-Thoughts & Architectural Review | [`docs/CONCLUSION.md`](CONCLUSION.md), [`README.md`](../README.md) | ✅ Completed |

---

## 2. High-Level Architecture Flow

```mermaid
graph LR
    User[👤 Passenger / Browser] -->|HTTP / HTTPS| EC2[☁️ Amazon EC2<br/>Flask App + Gunicorn]
    EC2 -->|IAM Role Authorization| IAM[🛡️ AWS IAM]
    EC2 -->|Boto3 Put/Get/Query| DDB[(🗄️ Amazon DynamoDB<br/>Users & Bookings Tables)]
    EC2 -->|Boto3 Publish| SNS[📢 Amazon SNS<br/>BookingConfirmation Topic]
    SNS -->|Instant Email Alert| Inbox[📧 Passenger Email Inbox]
```

---

## 3. Sequence Diagram 1: User Registration & Authentication (Epic 1 & 3)

```mermaid
sequenceDiagram
    autonumber
    actor User as Passenger
    participant UI as Browser / Frontend
    participant App as Flask Backend (EC2)
    participant DDB as DynamoDB (TravelGo_Users)

    Note over User, DDB: Registration Flow
    User->>UI: Fills Register Form (Name, Email, Phone, Password)
    UI->>App: POST /auth/register
    App->>App: Hash password (PBKDF2/Werkzeug)
    App->>DDB: PutItem with Condition (email not exists)
    alt User Already Exists
        DDB-->>App: ConditionalCheckFailedException
        App-->>UI: 400 Bad Request ("Email already registered")
    else User is New
        DDB-->>App: 200 OK (User created, logins=1)
        App-->>UI: Redirect to /auth/login with Success message
    end

    Note over User, DDB: Login Flow
    User->>UI: Enters Email & Password
    UI->>App: POST /auth/login
    App->>DDB: GetItem(email)
    DDB-->>App: Returns User Item (hashed password)
    App->>App: Verify Password Hash
    alt Credentials Valid
        App->>DDB: UpdateItem (increment logins count)
        App->>App: Set session['user_email'] & session['user_name']
        App-->>UI: Redirect to /dashboard
    else Invalid Password
        App-->>UI: 401 Unauthorized ("Invalid email or password")
    end
```

---

## 4. Sequence Diagram 2: Multi-Mode Booking & Real-Time SNS Notification (Epic 1, 3 & 4)

```mermaid
sequenceDiagram
    autonumber
    actor User as Passenger
    participant UI as TravelGo UI
    participant App as Flask Backend (EC2)
    participant DDB as DynamoDB (TravelGo_Bookings)
    participant SNS as Amazon SNS (BookingConfirmation)
    actor Inbox as User Email Inbox

    User->>UI: Selects Travel Mode (Bus, Train, Flight, Hotel)
    UI->>App: GET /search?mode=bus&origin=Hyderabad&destination=Bangalore
    App-->>UI: Returns available inventory & interactive seat selector

    User->>UI: Selects Seats (e.g., 2A, 3A) & clicks "Book Now"
    UI->>App: POST /book (mode, origin, destination, seats, price)

    App->>App: Generate Booking ID (BK-XXXX) & Transaction ID (TXN-XXXX)
    App->>DDB: PutItem in TravelGo_Bookings<br/>(booking_id, email, type, source, destination, date, seat, price, status='CONFIRMED')
    DDB-->>App: 200 OK (Item Saved)

    Note over App, SNS: Epic 4: Real-time SNS Trigger
    App->>SNS: Publish(TopicArn='BookingConfirmation',<br/>Subject='TravelGo: Booking Confirmed (BK-XXXX)',<br/>Message=Full Booking Summary)
    SNS-->>App: MessageId returned
    SNS--)Inbox: Sends instant email confirmation alert
    
    App-->>UI: Redirect to /booking-confirmation/<booking_id>
```

---

## 5. Sequence Diagram 3: Travel History Dashboard & Cancellation Workflow (Epic 1, 3 & 4)

```mermaid
sequenceDiagram
    autonumber
    actor User as Passenger
    participant UI as Dashboard UI
    participant App as Flask Backend (EC2)
    participant DDB as DynamoDB (TravelGo_Bookings)
    participant SNS as Amazon SNS (BookingConfirmation)
    actor Inbox as User Email Inbox

    User->>UI: Navigates to /dashboard
    UI->>App: GET /dashboard (Session: user_email)
    App->>DDB: Query(IndexName='UserBookingsIndex',<br/>KeyConditionExpression='user_email = :email')
    DDB-->>App: List of User Bookings (Sorted newest first)
    App-->>UI: Render Dashboard with Categorized Tabs (Bus, Train, Flight, Hotel)

    User->>UI: Clicks "Cancel Booking" on Booking BK-XXXX
    UI->>App: POST /cancel-booking/<booking_id>
    App->>DDB: UpdateItem(booking_id, status='CANCELLED', cancelled_at=timestamp)
    DDB-->>App: Item Updated

    App->>SNS: Publish(TopicArn='BookingConfirmation',<br/>Subject='TravelGo: Booking Cancelled (BK-XXXX)',<br/>Message=Cancellation Details)
    SNS--)Inbox: Sends instant cancellation email alert
    App-->>UI: Redirect to /dashboard with Success alert
```
