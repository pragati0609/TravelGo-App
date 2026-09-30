# AWS DynamoDB Tables Setup Script for TravelGo
# Task 7: Create DynamoDB tables for storing registration details and booking records
# Run this script once to provision both tables in your AWS account.
# Requires: AWS credentials configured (via IAM role on EC2, or ~/.aws/credentials locally)

import os
import sys
import boto3
from botocore.exceptions import ClientError

def create_tables():
    region = os.environ.get('AWS_REGION', 'ap-south-1')
    users_table = os.environ.get('DYNAMODB_USERS_TABLE', 'TravelGo_Users')
    bookings_table = os.environ.get('DYNAMODB_BOOKINGS_TABLE', 'TravelGo_Bookings')

    print(f"Connecting to AWS DynamoDB in region: {region}")
    dynamodb = boto3.resource('dynamodb', region_name=region)
    client = boto3.client('dynamodb', region_name=region)

    existing_tables = client.list_tables()['TableNames']
    print(f"Existing tables: {existing_tables}")

    # ─── Table 1: TravelGo_Users ──────────────────────────────────────────────
    if users_table in existing_tables:
        print(f"[SKIP] Table '{users_table}' already exists.")
    else:
        print(f"Creating table '{users_table}'...")
        table = dynamodb.create_table(
            TableName=users_table,
            KeySchema=[
                {'AttributeName': 'email', 'KeyType': 'HASH'}   # Partition Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'email', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'   # On-demand pricing, no capacity planning needed
        )
        table.wait_until_exists()
        print(f"[OK] Table '{users_table}' created successfully.")

    # ─── Table 2: TravelGo_Bookings ───────────────────────────────────────────
    if bookings_table in existing_tables:
        print(f"[SKIP] Table '{bookings_table}' already exists.")
    else:
        print(f"Creating table '{bookings_table}' with GSI 'UserBookingsIndex'...")
        table = dynamodb.create_table(
            TableName=bookings_table,
            KeySchema=[
                {'AttributeName': 'booking_id', 'KeyType': 'HASH'}  # Partition Key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'booking_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_email',  'AttributeType': 'S'},
                {'AttributeName': 'created_at',  'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'UserBookingsIndex',       # GSI for user dashboard queries
                    'KeySchema': [
                        {'AttributeName': 'user_email', 'KeyType': 'HASH'},
                        {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        table.wait_until_exists()
        print(f"[OK] Table '{bookings_table}' with GSI created successfully.")

    print("\nDynamoDB Setup Complete!")
    print(f"  Users Table     : {users_table}")
    print(f"  Bookings Table  : {bookings_table}")
    print(f"  GSI             : UserBookingsIndex (user_email PK, created_at SK)")

if __name__ == '__main__':
    try:
        create_tables()
    except ClientError as e:
        print(f"AWS Error: {e.response['Error']['Message']}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
