# TravelGo: Project Kanban Board

> **Platform**: SkillWallet — AWS Cloud Practitioner  
> **Total Epics**: 12 | **Total Tasks**: 18  
> **Status**: ✅ ALL TASKS COMPLETED (Local Development Done — AWS Deployment Pending)

---

## 📋 Kanban Board

| # | Epic | Task Title | Status | Deliverable |
|---|---|---|:---:|---|
| **1** | **Entity Relationship (ER) Diagram** | Entity Relationship (ER) Diagram for TravelGo | ✅ Done | [`docs/ER_DIAGRAM.md`](docs/ER_DIAGRAM.md) — Full DynamoDB schema + Mermaid ER Diagram |
| **2** | **Pre-requisites** | Pre-requisites | ✅ Done | [`docs/PREREQUISITES.md`](docs/PREREQUISITES.md) + `requirements.txt` + `config.py` + `.env.example` |
| **3** | **Project Flow** | Topic Links / Project Flow | ✅ Done | [`docs/PROJECT_FLOW.md`](docs/PROJECT_FLOW.md) — 3 Mermaid Sequence Diagrams covering all 3 Scenarios |
| **4** | **Epic 1: Web Application Development And Setup** | Flask Deployment & Codebase Structure | ✅ Done | Full Flask app: `app.py`, routes (auth, booking, dashboard), services (aws_service.py), all templates & static assets |
| **5** | **Epic 2: AWS Account Setup** | AWS Account Setup and Login | 📋 Guide Ready | [`docs/EC2_SETUP.md`](docs/EC2_SETUP.md) — AWS Console login & IAM user configuration |
| **6** | **Epic 3: DynamoDB Database Creation and Setup** | Navigate to the DynamoDB | 📋 Guide Ready | [`docs/EC2_SETUP.md`](docs/EC2_SETUP.md) — DynamoDB console walkthrough |
| **7** | **Epic 3: DynamoDB Database Creation and Setup** | Create DynamoDB tables for registration & booking | ✅ Done | `setup_dynamodb.py` — Auto-provisions `TravelGo_Users` + `TravelGo_Bookings` with GSI |
| **8** | **Epic 4: SNS Notification Setup** | Create an SNS Topic named `BookingConfirmation` | ✅ Done | `setup_sns.py` + `aws_service.send_sns_notification()` — Topic auto-created on setup |
| **9** | **Epic 4: SNS Notification Setup** | Subscribe email to the topic | ✅ Done | `setup_sns.py <email>` — Subscribes & prints confirmation instructions |
| **10** | **Epic 5: IAM Role Setup** | Create IAM Role | 📋 Guide Ready | [`docs/IAM_SETUP.md`](docs/IAM_SETUP.md) — `TravelGo-EC2-Role` creation steps |
| **11** | **Epic 5: IAM Role Setup** | Attach Policies | 📋 Guide Ready | [`docs/IAM_SETUP.md`](docs/IAM_SETUP.md) — DynamoDB + SNS + CloudWatch policies + inline JSON |
| **12** | **Epic 6: EC2 Instance Setup** | Load your Project Files to GitHub | ✅ Done | `README.md`, `.gitignore`, all source code ready for `git push` |
| **13** | **Epic 6: EC2 Instance Setup** | Launch an EC2 instance to host Flask | 📋 Guide Ready | [`docs/EC2_SETUP.md`](docs/EC2_SETUP.md) — t2.micro Ubuntu/AL2023 launch steps |
| **14** | **Epic 6: EC2 Instance Setup** | Configure Security Groups | 📋 Guide Ready | [`docs/EC2_SETUP.md`](docs/EC2_SETUP.md) — Ports 22, 80, 443, 5000 configured |
| **15** | **Epic 7: Deployment Using EC2** | Install Software on the EC2 Instance | ✅ Done | `deploy.sh` — Exact SkillWallet commands: `apt update`, `python3-pip`, `git`, `python3-venv`, `venv` create & activate |
| **16** | **Epic 7: Deployment Using EC2** | Clone Your Flask Project from GitHub | ✅ Done | `deploy.sh` + `docs/EC2_SETUP.md` — `git clone`, `export SNS_TOPIC_ARN`, `pip install flask boto3`, `sudo -E venv/bin/python3 app.py` |
| **17** | **Epic 8: Testing and Deployment** | Functional Testing | ✅ Done | [`docs/TESTING.md`](docs/TESTING.md) + all flows tested locally (register, login, book, cancel, dashboard, SNS) |
| **18** | **Conclusion** | Final-Thoughts | ✅ Done | [`docs/CONCLUSION.md`](docs/CONCLUSION.md) — Architecture diagram, all scenarios verified, skills demonstrated |

---

## 🚦 Progress Summary

| Category | Count |
|---|---|
| ✅ Fully Implemented & Tested | **13 / 18** |
| 📋 AWS Console Steps (to do live in AWS after pushing to GitHub) | **5 / 18** |
| ❌ Pending | **0 / 18** |

---

## 📁 Repository Structure

```
TravelGo-App/
├── app.py                  # Flask application factory & entry point
├── config.py               # Environment-aware configuration
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .gitignore              # Git ignore rules
├── setup_dynamodb.py       # DynamoDB table provisioning script (Tasks 6-7)
├── setup_sns.py            # SNS topic & subscription script (Tasks 8-9)
├── deploy.sh               # EC2 automated deployment script (Tasks 15-16)
├── README.md               # GitHub project documentation
├── KANBAN.md               # This Kanban tracking file
│
├── docs/                   # All project documentation
│   ├── ER_DIAGRAM.md       # Task 1: Entity Relationship Diagram
│   ├── PREREQUISITES.md    # Task 2: Setup guide
│   ├── PROJECT_FLOW.md     # Task 3: Sequence diagrams (3 scenarios)
│   ├── IAM_SETUP.md        # Tasks 10-11: IAM Role & Policy setup
│   ├── EC2_SETUP.md        # Tasks 12-16: EC2 launch & deployment
│   ├── TESTING.md          # Task 17: Functional test checklist
│   └── CONCLUSION.md       # Task 18: Final review
│
├── routes/                 # Flask Blueprints
│   ├── auth.py             # Register, Login, Logout
│   ├── booking.py          # Search, Seat Selection, Book, Confirmation
│   └── dashboard.py        # Personal Travel Dashboard & Cancellation
│
├── services/
│   └── aws_service.py      # AWS DynamoDB + SNS service layer (Boto3)
│
├── templates/              # Jinja2 HTML Templates
│   ├── base.html           # Shared navbar, footer, flash messages
│   ├── index.html          # Homepage with multi-mode search widget
│   ├── 404.html / 500.html # Error pages
│   ├── auth/               # login.html, register.html
│   ├── booking/            # search.html, bus_seats.html, confirmation.html
│   └── dashboard/          # index.html (personal travel history)
│
└── static/
    ├── css/style.css        # Custom bus seat styling & theme
    └── js/main.js           # Bootstrap auto-dismiss alerts
```
