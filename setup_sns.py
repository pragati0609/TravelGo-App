# AWS SNS Topic Setup Script for TravelGo
# Task 8-9: Create 'BookingConfirmation' SNS topic and subscribe your email endpoint
# Run this script to provision SNS and then check your inbox for the confirmation email.

import os
import sys
import boto3
from botocore.exceptions import ClientError

def setup_sns(subscriber_email: str):
    region = os.environ.get('AWS_REGION', 'ap-south-1')
    topic_name = 'BookingConfirmation'

    print(f"Setting up SNS in region: {region}")
    sns = boto3.client('sns', region_name=region)

    # ─── Step 1: Create the standard SNS Topic ────────────────────────────────
    print(f"Creating SNS topic: '{topic_name}'...")
    response = sns.create_topic(Name=topic_name)
    topic_arn = response['TopicArn']
    print(f"[OK] SNS Topic ARN: {topic_arn}")

    # ─── Step 2: Subscribe email endpoint to the topic ────────────────────────
    print(f"Subscribing email: {subscriber_email}...")
    sub_response = sns.subscribe(
        TopicArn=topic_arn,
        Protocol='email',
        Endpoint=subscriber_email,
        ReturnSubscriptionArn=True
    )
    sub_arn = sub_response.get('SubscriptionArn', 'PendingConfirmation')
    print(f"[OK] Subscription ARN: {sub_arn}")
    print()
    print("=" * 60)
    print("IMPORTANT NEXT STEP:")
    print(f"  AWS has sent a confirmation email to: {subscriber_email}")
    print("  Open the email and click 'Confirm subscription' before")
    print("  SNS can deliver notifications to your inbox.")
    print("=" * 60)
    print()
    print("Update your .env file with:")
    print(f"  SNS_TOPIC_ARN={topic_arn}")

    return topic_arn

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python setup_sns.py <your-email@example.com>")
        sys.exit(1)
    try:
        email = sys.argv[1]
        setup_sns(email)
    except ClientError as e:
        print(f"AWS Error: {e.response['Error']['Message']}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
