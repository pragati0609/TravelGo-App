# TravelGo: AWS Account Setup Guide

> **Epic 2**: AWS Account Setup and Login — Task 5  
> **SkillWallet Course**: AWS Cloud Practitioner

---

> [!IMPORTANT]  
> **Course Notice**: *This is for your understanding only, please refrain from creating a personal AWS account. A temporary AWS account will be provided via Troven on your course portal.*

---

## 1. AWS Account Creation Walkthrough (Reference)

For standard reference and conceptual understanding:

1. **Visit AWS**: Go to the AWS website ([https://aws.amazon.com/](https://aws.amazon.com/)).
2. **Start Registration**: Click on the **"Create an AWS Account"** button.
3. **Credentials**: Follow the prompts to enter your email address and choose a strong password.
4. **Account Information**: Provide the required account information, including your full name, address, and phone number.
5. **Payment Information**: Enter payment details. *(Note: While AWS offers a free tier, a valid debit or credit card is required for identity verification).*
6. **Identity Verification**: Complete the phone call / SMS identity verification process.
7. **Support Plan**: Choose the **Basic Support Plan** (Free tier eligible, sufficient for learning and project deployment).
8. **Account Ready**: Once verified, your account is activated and ready for access.

---

## 2. Log In to the AWS Management Console

1. Navigate to the **[AWS Management Console](https://aws.amazon.com/console/)** (or click the login link provided inside your Troven lab dashboard).
2. Enter your credentials:
   - If using Troven temporary credentials: Log in as **IAM User** with the provided Account ID, Username, and Password.
   - If using direct login: Sign in as Root or IAM user.
3. Set your active region in the navigation bar to **Asia Pacific (Mumbai) `ap-south-1`** (or the default region specified by your lab).

---

## 3. Environment Variable Alignment

When deploying locally or configuring your EC2 instance, ensure the AWS region matches your console:

In [`.env`](../.env):
```env
AWS_REGION=ap-south-1
```
*(Leave `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` empty when running on EC2 with an attached IAM Role, as temporary tokens are fetched automatically).*
