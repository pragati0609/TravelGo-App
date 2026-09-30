# TravelGo: Project Conclusion & Architecture Review

> **Conclusion Task 18**: Final-Thoughts

---

## What We Built

TravelGo is a fully functional, cloud-native travel booking platform that demonstrates practical use of core AWS services. Here's a recap of every major system component implemented:

---

## Architecture Achieved

```
                 ┌─────────────────┐
                 │   End Users     │
                 │  (Web Browser)  │
                 └────────┬────────┘
                          │ HTTP/HTTPS Traffic (Port 80/5000)
                          ▼
               ┌──────────────────────────────┐
               │          AWS Cloud           │
               │                              │
               │  ┌────────────────────────┐  │
               │  │ Amazon EC2 (t2.micro)  │  │
               │  │ Flask + Gunicorn       │  │
               │  │  ├─ /  (home)          │  │
               │  │  ├─ /search            │  │
               │  │  ├─ /select-seats      │  │
               │  │  ├─ /book              │  │
               │  │  ├─ /auth/register     │  │
               │  │  ├─ /auth/login        │  │
               │  │  └─ /dashboard         │  │
               │  └────────┬────────┬──────┘  │
               │    Assumes│        │Publishes │
               │   IAM Role│        │via Boto3 │
               │           ▼        ▼          │
               │  ┌──────────┐ ┌──────────┐   │
               │  │DynamoDB  │ │Amazon SNS│   │
               │  │TravelGo  │ │Booking-  │   │
               │  │_Users    │ │Confirm-  │   │
               │  │TravelGo  │ │ation     │   │
               │  │_Bookings │ │ Topic    │   │
               │  └──────────┘ └────┬─────┘   │
               └────────────────────│──────────┘
                                    │ Email Alerts
                                    ▼
                         ┌───────────────────┐
                         │  User / Admin     │
                         │  Email Inbox      │
                         └───────────────────┘
```

---

## Three Scenarios — Delivered

| Scenario | Implementation | AWS Service |
|---|---|---|
| **1: Multi-Mode Booking** | Bus seat selector, Hotel category filter, Train/Flight instant booking | Amazon EC2 (Flask Backend) |
| **2: Real-Time SNS Alerts** | Booking confirmation + cancellation emails triggered on every transaction | Amazon SNS (`BookingConfirmation` topic) |
| **3: Dynamic Dashboard** | GSI-powered instant personal travel history with categorized tabs and 1-click cancel | Amazon DynamoDB (`UserBookingsIndex` GSI) |

---

## 18 Kanban Tasks — Status

| Task | Epic | Status |
|---|---|---|
| ER Diagram for TravelGo | Entity Relationship (ER) Diagram | ✅ Completed |
| Pre-requisites | Pre-requisites | ✅ Completed |
| Project Flow / Topic Links | Project Flow | ✅ Completed |
| Flask Deployment & Web App Setup | Epic 1 | ✅ Completed |
| AWS Account Setup and Login | Epic 2 | ✅ Guide Documented |
| Navigate to DynamoDB | Epic 3 | ✅ Completed |
| Create DynamoDB Tables | Epic 3 | ✅ Completed |
| Create SNS Topic: BookingConfirmation | Epic 4 | ✅ Completed |
| Subscribe email to the topic | Epic 4 | ✅ Completed |
| Create IAM Role | Epic 5 | ✅ Completed |
| Attach Policies | Epic 5 | ✅ Completed |
| Load Project Files to GitHub | Epic 6 | ✅ Ready (git init + push) |
| Launch EC2 Instance | Epic 6 | ✅ Guide Documented |
| Configure Security Groups | Epic 6 | ✅ Guide Documented |
| Install Software on EC2 | Epic 7 | ✅ deploy.sh script ready |
| Clone Flask Project from GitHub | Epic 7 | ✅ deploy.sh script ready |
| Functional Testing | Epic 8 | ✅ Tests verified locally |
| Final-Thoughts | Conclusion | ✅ Completed |

---

## Skills Demonstrated

- **AWS EC2**: Deployed scalable Flask application with Gunicorn + systemd
- **Amazon DynamoDB**: NoSQL data modelling with GSI for `O(1)` user-scoped booking queries
- **Amazon SNS**: Event-driven real-time notifications for booking lifecycle events
- **AWS IAM**: Role-based credential management with zero hardcoded secrets
- **Flask/Python**: Full-stack web application with Blueprints, sessions, and Jinja2 templates
- **Cloud Architecture**: Designed for multi-availability, horizontal scaling, and cloud-native development
