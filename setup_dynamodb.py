# AWS DynamoDB Tables Setup Script for TravelGo
# Epic 3: DynamoDB Database Creation and Setup
#
# Creates:
#   1. Table: travel-Users
#      Partition Key: Email (String)
#   2. Table: Bookings
#      Partition Key: email (String)
#      Sort Key:      booking_id (String)

import os
import sys
import boto3
from botocore.exceptions import ClientError

def create_tables():
    region = os.environ.get('AWS_REGION', 'ap-south-1')
    users_table = os.environ.get('DYNAMODB_USERS_TABLE', 'travel-Users')
    bookings_table = os.environ.get('DYNAMODB_BOOKINGS_TABLE', 'Bookings')

    print(f"Connecting to AWS DynamoDB in region: {region}")
    dynamodb = boto3.resource('dynamodb', region_name=region)
    client = boto3.client('dynamodb', region_name=region)

    existing_tables = client.list_tables().get('TableNames', [])
    print(f"Existing tables in {region}: {existing_tables}")

    # ─── Table 1: travel-Users ────────────────────────────────────────────────
    # Partition Key: "Email" (String)
    if users_table in existing_tables:
        print(f"[SKIP] Table '{users_table}' already exists.")
    else:
        print(f"Creating table '{users_table}' with Partition Key 'Email'...")
        table = dynamodb.create_table(
            TableName=users_table,
            KeySchema=[
                {'AttributeName': 'Email', 'KeyType': 'HASH'}   # Partition Key: Email (String)
            ],
            AttributeDefinitions=[
                {'AttributeName': 'Email', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'   # On-demand pricing, no capacity planning needed
        )
        table.wait_until_exists()
        print(f"[OK] Table '{users_table}' created successfully.")

    # ─── Table 2: Bookings ───────────────────────────────────────────────────
    # Partition Key: "email" (String), Sort Key: "booking_id" (String)
    if bookings_table in existing_tables:
        print(f"[SKIP] Table '{bookings_table}' already exists.")
    else:
        print(f"Creating table '{bookings_table}' with Partition Key 'email' and Sort Key 'booking_id'...")
        table = dynamodb.create_table(
            TableName=bookings_table,
            KeySchema=[
                {'AttributeName': 'email', 'KeyType': 'HASH'},      # Partition Key: email (String)
                {'AttributeName': 'booking_id', 'KeyType': 'RANGE'} # Sort Key: booking_id (String)
            ],
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'},
                {'AttributeName': 'booking_id', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print(f"[OK] Table '{bookings_table}' created successfully.")

    print("\nDynamoDB Setup Complete!")
    print(f"  Users Table     : {users_table} (PK: Email [S])")
    print(f"  Bookings Table  : {bookings_table} (PK: email [S], SK: booking_id [S])")

if __name__ == '__main__':
    try:
        create_tables()
    except ClientError as e:
        print(f"AWS Error: {e.response['Error']['Message']}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
