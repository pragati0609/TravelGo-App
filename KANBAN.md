# TravelGo: A Cloud-Powered Real-Time Travel Booking Platform Using AWS
## Project Kanban & Implementation Roadmap

> **Platform**: SkillWallet - AWS Cloud Practitioner
> **Status**: In Progress | Total Epics: 12 | Total Tasks: 18

---

## 📋 Kanban Board Breakdown

| # | Epic | Task Title | Status | Description / Deliverable |
|---|---|---|:---:|---|
| **1** | **Entity Relationship (ER) Diagram** | Entity Relationship (ER) Diagram for TravelGo | ✅ **Completed** | Full ER schema defining `TravelGo_Users`, `TravelGo_Bookings`, and `TravelGo_Listings` in [`docs/ER_DIAGRAM.md`](file:///C:/My%20Projects/TravelGo/TravelGo-App/docs/ER_DIAGRAM.md). |
| **2** | **Pre-requisites** | Pre-requisites | ⏳ Ready | Environment setup: Python 3.9+, Flask, Boto3, AWS CLI, AWS credentials. |
| **3** | **Project Flow** | Topic Links / Project Flow | ⏳ Ready | End-to-end architecture flow from Web UI -> EC2 Flask -> DynamoDB & SNS. |
| **4** | **Epic 1: Web Application Development And Setup** | Flask Deployment & Codebase Structure | ⏳ Ready | Complete Flask application with multi-mode booking (Bus seat selector, Hotels, Flights, Trains), Auth, and Dashboard. |
| **5** | **Epic 2: AWS Account Setup** | AWS Account Setup and Login | ⏳ Ready | AWS Management Console login and IAM user / CLI profile configuration. |
| **6** | **Epic 3: DynamoDB Database Creation and Setup** | Navigate to the DynamoDB | ⏳ Ready | Access DynamoDB console in AWS region (e.g., `us-east-1` or `ap-south-1`). |
| **7** | **Epic 3: DynamoDB Database Creation and Setup** | Create DynamoDB tables for registration & booking | ⏳ Ready | Create `TravelGo_Users` (Partition Key: `email`) and `TravelGo_Bookings` (Partition Key: `booking_id`). |
| **8** | **Epic 4: SNS Notification Setup** | Create an SNS Topic named `BookingConfirmation` | ⏳ Ready | Set up standard SNS Topic `BookingConfirmation` for notifications. |
| **9** | **Epic 4: SNS Notification Setup** | Subscribe email to the topic | ⏳ Ready | Subscribe user/admin email endpoint to SNS topic and confirm subscription. |
| **10** | **Epic 5: IAM Role Setup** | Create IAM Role | ⏳ Ready | Create EC2 Service Role (`TravelGo-EC2-Role`). |
| **11** | **Epic 5: IAM Role Setup** | Attach Policies | ⏳ Ready | Attach policies for `AmazonDynamoDBFullAccess` (or custom scoped) and `AmazonSNSFullAccess`. |
| **12** | **Epic 6: EC2 Instance Setup** | Load your Project Files to GitHub | ⏳ Ready | Initialize git repository and push source code to GitHub. |
| **13** | **Epic 6: EC2 Instance Setup** | Launch an EC2 instance to host Flask | ⏳ Ready | Launch an Amazon Linux 2023 / Ubuntu `t2.micro` or `t3.micro` instance with attached IAM role. |
| **14** | **Epic 6: EC2 Instance Setup** | Configure Security Groups | ⏳ Ready | Inbound rules: SSH (Port 22), HTTP (Port 80), Custom TCP (Port 5000). |
| **15** | **Epic 7: Deployment Using EC2** | Install Software on EC2 Instance | ⏳ Ready | EC2 user data / terminal setup script: `python3`, `pip`, `git`, virtual environment, dependencies. |
| **16** | **Epic 7: Deployment Using EC2** | Clone Your Flask Project from GitHub | ⏳ Ready | Clone repository onto EC2, configure `.env`, start application with Gunicorn/Systemd. |
| **17** | **Epic 8: Testing and Deployment** | Functional Testing | ⏳ Ready | Verify registration, login, bus seat selection, booking confirmation, DynamoDB records, and SNS email alerts. |
| **18** | **Conclusion** | Final-Thoughts | ⏳ Ready | Project wrap-up, architecture review, and submission documentation. |

---

## 🏛️ Technical Architecture Summary

```
                      +-------------------+
                      |     End User      |
                      |   (Web Browser)   |
                      +---------+---------+
                                |
                     HTTP/HTTPS | (Port 80 / 5000)
                                v
               +---------------------------------+
               |            AWS Cloud            |
               |                                 |
               |   +--------------------------+  |
               |   |   Amazon EC2 Instance    |  |
               |   |   (Flask App Backend)    |  |
               |   +------------+-------------+  |
               |         |      |     ^          |
               |         |      |     |          |
               |   Assumes      |     |          |
               |   IAM Role     |     |          |
               |   (EC2)        |     |          |
               |         |      |     |          |
               |         v      v     |          |
               |   +----------+  +----+--------+ |
               |   | DynamoDB |  |   Amazon    | |
               |   | Tables   |  |     SNS     | |
               |   | (Auth &  |  |  (Topic:    | |
               |   | Bookings)|  | Booking-    | |
               |   +----------+  | Confirmation) |
               |                 +-----+-------+ |
               +-----------------------|---------+
                                       |
                                       v Email Alerts
                            +--------------------+
                            | User/Admin Email   |
                            | (Confirmed/Cancel) |
                            +--------------------+
```
