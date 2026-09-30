import os
import uuid
from datetime import datetime, timezone
import logging
from werkzeug.security import generate_password_hash, check_password_hash
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

logger = logging.getLogger(__name__)

class AWSService:
    """Encapsulates AWS DynamoDB and SNS interactions for TravelGo."""

    def __init__(self, app=None):
        self.app = app
        self.region = os.environ.get('AWS_REGION', 'ap-south-1')
        self.users_table_name = os.environ.get('DYNAMODB_USERS_TABLE', 'travel-Users')
        self.bookings_table_name = os.environ.get('DYNAMODB_BOOKINGS_TABLE', 'Bookings')
        self.sns_topic_arn = os.environ.get('SNS_TOPIC_ARN', '')
        self.use_mock = os.environ.get('USE_MOCK_AWS', 'auto').lower()

        # In-memory mock storage if live AWS is unreachable or configured for offline
        self._mock_users = {}
        self._mock_bookings = {}
        self._is_live_aws = False

        self._init_clients()

    def _init_clients(self):
        """Initializes Boto3 clients or activates mock mode if credentials aren't set."""
        if self.use_mock == 'true':
            logger.info("USE_MOCK_AWS is explicitly 'true'. Running in offline mock mode.")
            self._is_live_aws = False
            return

        try:
            # If access keys are provided via .env, pass them explicitly; otherwise boto3 automatically
            # discovers credentials from environment, ~/.aws/credentials, or EC2 IAM Instance Profile!
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

            session_kwargs = {'region_name': self.region}
            if aws_access_key and aws_secret_key:
                session_kwargs['aws_access_key_id'] = aws_access_key
                session_kwargs['aws_secret_access_key'] = aws_secret_key

            session = boto3.Session(**session_kwargs)
            self.dynamodb = session.resource('dynamodb')
            self.dynamodb_client = session.client('dynamodb')
            self.sns_client = session.client('sns')

            # Quick probe to test connectivity
            self.dynamodb_client.list_tables()
            self._is_live_aws = True
            logger.info(f"Successfully connected to AWS in region {self.region}!")
        except (NoCredentialsError, ClientError, Exception) as e:
            logger.warning(f"Live AWS connectivity not available ({e}). Falling back to in-memory cloud simulator for seamless local development.")
            self._is_live_aws = False

    # -------------------------------------------------------------
    # Table Setup
    # -------------------------------------------------------------
    def create_tables_if_not_exist(self):
        """Creates DynamoDB tables and GSIs as specified in the course requirements."""
        if not self._is_live_aws:
            return {"status": "mock_ready", "message": "Using in-memory mock DynamoDB."}

        created = []
        try:
            existing = self.dynamodb_client.list_tables()['TableNames']

            # 1. Users Table
            if self.users_table_name not in existing:
                self.dynamodb.create_table(
                    TableName=self.users_table_name,
                    KeySchema=[{'AttributeName': 'email', 'KeyType': 'HASH'}],
                    AttributeDefinitions=[{'AttributeName': 'email', 'AttributeType': 'S'}],
                    BillingMode='PAY_PER_REQUEST'
                )
                created.append(self.users_table_name)

            # 2. Bookings Table with UserBookingsIndex GSI
            if self.bookings_table_name not in existing:
                self.dynamodb.create_table(
                    TableName=self.bookings_table_name,
                    KeySchema=[{'AttributeName': 'booking_id', 'KeyType': 'HASH'}],
                    AttributeDefinitions=[
                        {'AttributeName': 'booking_id', 'AttributeType': 'S'},
                        {'AttributeName': 'user_email', 'AttributeType': 'S'},
                        {'AttributeName': 'created_at', 'AttributeType': 'S'}
                    ],
                    GlobalSecondaryIndexes=[
                        {
                            'IndexName': 'UserBookingsIndex',
                            'KeySchema': [
                                {'AttributeName': 'user_email', 'KeyType': 'HASH'},
                                {'AttributeName': 'created_at', 'KeyType': 'RANGE'}
                            ],
                            'Projection': {'ProjectionType': 'ALL'}
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                created.append(self.bookings_table_name)

            return {"status": "success", "created_tables": created}
        except Exception as e:
            logger.error(f"Error creating DynamoDB tables: {e}")
            return {"status": "error", "error": str(e)}

    # -------------------------------------------------------------
    # User Authentication & Management
    # -------------------------------------------------------------
    def register_user(self, email, password, full_name, phone=""):
        """Registers a new user in DynamoDB with a hashed password."""
        email = email.strip().lower()
        now = datetime.now(timezone.utc).isoformat()
        password_hash = generate_password_hash(password)
        user_id = str(uuid.uuid4())

        user_item = {
            'Email': email,                     # Exact PK for travel-Users (SkillWallet)
            'email': email,                     # Lowercase alias
            'user_id': user_id,
            'name': full_name.strip(),          # Exact ER Diagram attribute
            'full_name': full_name.strip(),     # Display alias
            'phone': phone.strip(),
            'password': password_hash,          # Exact ER Diagram attribute
            'password_hash': password_hash,
            'logins': 1,                        # Exact ER Diagram attribute (login counter)
            'role': 'user',
            'created_at': now,
            'updated_at': now
        }

        if self._is_live_aws:
            try:
                table = self.dynamodb.Table(self.users_table_name)
                # Ensure user does not already exist
                table.put_item(
                    Item=user_item,
                    ConditionExpression='attribute_not_exists(email)'
                )
                return {"success": True, "user_id": user_id, "email": email}
            except ClientError as e:
                if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                    return {"success": False, "error": "An account with this email already exists."}
                return {"success": False, "error": str(e)}
        else:
            if email in self._mock_users:
                return {"success": False, "error": "An account with this email already exists."}
            self._mock_users[email] = user_item
            return {"success": True, "user_id": user_id, "email": email}

    def authenticate_user(self, email, password):
        """Verifies email and password against DynamoDB."""
        email = email.strip().lower()

        user = None
        if self._is_live_aws:
            try:
                table = self.dynamodb.Table(self.users_table_name)
                response = table.get_item(Key={'email': email})
                user = response.get('Item')
            except Exception as e:
                logger.error(f"DynamoDB get_item error: {e}")
                return {"success": False, "error": str(e)}
        else:
            user = self._mock_users.get(email)

        if not user:
            return {"success": False, "error": "Invalid email or password."}

        if check_password_hash(user['password_hash'], password):
            # Increment logins count as per ER diagram specification
            current_logins = user.get('logins', 1) + 1
            user['logins'] = current_logins
            if self._is_live_aws:
                try:
                    table = self.dynamodb.Table(self.users_table_name)
                    table.update_item(
                        Key={'email': email},
                        UpdateExpression="SET logins = logins + :val",
                        ExpressionAttributeValues={':val': 1}
                    )
                except Exception as e:
                    logger.warning(f"Could not update logins count in DynamoDB: {e}")

            return {
                "success": True,
                "user": {
                    "email": user['email'],
                    "name": user.get('name', user.get('full_name', '')),
                    "full_name": user.get('full_name', ''),
                    "logins": current_logins,
                    "phone": user.get('phone', ''),
                    "role": user.get('role', 'user')
                }
            }
        return {"success": False, "error": "Invalid email or password."}

    # -------------------------------------------------------------
    # Bookings Management (Scenario 1 & 3)
    # -------------------------------------------------------------
    def create_booking(self, user_email, booking_data):
        """Creates a travel booking and triggers an instant SNS notification."""
        booking_id = f"BK-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc).isoformat()
        txn_ref = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        b_type = booking_data.get('travel_mode', 'bus')
        b_source = booking_data.get('origin', '')
        b_destination = booking_data.get('destination', '')
        b_date = booking_data.get('travel_date', '')
        b_seat = booking_data.get('seat_numbers', '') or booking_data.get('room_preference', '')
        b_details = booking_data.get('provider_name', 'TravelGo Express')
        b_price = int(booking_data.get('total_amount', 0))

        item = {
            # --- Exact ER Diagram Attributes (SkillWallet Schema) ---
            'booking_id': booking_id,                           # PK
            'email': user_email.strip().lower(),                # FK referencing Users(email)
            'type': b_type,                                     # bus | train | flight | hotel
            'source': b_source,                                 # Origin location
            'destination': b_destination,                       # Destination location
            'date': b_date,                                     # Date of travel
            'seat': b_seat,                                     # Seat number or room tier
            'details': b_details,                               # Carrier / Hotel name
            'price': b_price,                                   # Total cost
            'payment_method': booking_data.get('payment_method', 'Credit Card / UPI'),
            'payment_reference': txn_ref,                       # Unique transaction ID

            # --- DynamoDB GSI & Platform Metadata ---
            'user_email': user_email.strip().lower(),           # GSI Partition Key
            'created_at': now,                                  # GSI Sort Key
            'travel_mode': b_type,
            'provider_name': b_details,
            'origin': b_source,
            'travel_date': b_date,
            'departure_time': booking_data.get('departure_time', '10:00 AM'),
            'arrival_time': booking_data.get('arrival_time', '06:00 PM'),
            'seat_numbers': b_seat,
            'room_preference': booking_data.get('room_preference', ''),
            'total_amount': b_price,
            'currency': 'INR',
            'booking_status': 'CONFIRMED',
            'payment_status': 'PAID',
            'sns_message_id': None,
            'cancelled_at': None
        }

        # Scenario 2: Real-Time Booking Confirmation via AWS SNS
        notification_res = self.send_sns_notification(
            subject=f"TravelGo: Booking Confirmed ({booking_id})",
            message=(
                f"Dear Customer,\n\n"
                f"Your travel booking with TravelGo is CONFIRMED!\n\n"
                f"--- Booking Details ---\n"
                f"Booking ID: {booking_id}\n"
                f"Mode: {item['travel_mode'].upper()}\n"
                f"Operator/Hotel: {item['provider_name']}\n"
                f"Route: {item['origin']} -> {item['destination']}\n"
                f"Date: {item['travel_date']}\n"
                f"{'Seats: ' + item['seat_numbers'] if item['seat_numbers'] else 'Room: ' + item['room_preference']}\n"
                f"Total Fare: Rs. {item['total_amount']}\n"
                f"Status: {item['booking_status']}\n\n"
                f"Thank you for choosing TravelGo!\n"
                f"Cloud-Powered Travel Booking Platform on AWS"
            )
        )

        if notification_res.get('success'):
            item['sns_message_id'] = notification_res.get('message_id')

        # Persist to DynamoDB
        if self._is_live_aws:
            try:
                table = self.dynamodb.Table(self.bookings_table_name)
                table.put_item(Item=item)
                return {"success": True, "booking": item}
            except Exception as e:
                logger.error(f"DynamoDB put_item booking error: {e}")
                return {"success": False, "error": str(e)}
        else:
            self._mock_bookings[booking_id] = item
            return {"success": True, "booking": item}

    def get_user_bookings(self, user_email):
        """Fetches all bookings for a user for the personal travel history dashboard."""
        user_email = user_email.strip().lower()

        if self._is_live_aws:
            try:
                table = self.dynamodb.Table(self.bookings_table_name)
                # Query using the Global Secondary Index for optimal O(1) partition search
                response = table.query(
                    IndexName='UserBookingsIndex',
                    KeyConditionExpression='user_email = :email',
                    ExpressionAttributeValues={':email': user_email},
                    ScanIndexForward=False  # Newest first
                )
                return {"success": True, "bookings": response.get('Items', [])}
            except Exception as e:
                logger.warning(f"GSI query failed, falling back to table scan: {e}")
                try:
                    response = table.scan(
                        FilterExpression='user_email = :email',
                        ExpressionAttributeValues={':email': user_email}
                    )
                    bookings = response.get('Items', [])
                    bookings.sort(key=lambda x: x.get('created_at', ''), reverse=True)
                    return {"success": True, "bookings": bookings}
                except Exception as e2:
                    return {"success": False, "error": str(e2), "bookings": []}
        else:
            items = [b for b in self._mock_bookings.values() if b['user_email'] == user_email]
            items.sort(key=lambda x: x['created_at'], reverse=True)
            return {"success": True, "bookings": items}

    def cancel_booking(self, booking_id, user_email):
        """Cancels an existing booking and dispatches an SNS cancellation alert."""
        user_email = user_email.strip().lower()
        now = datetime.now(timezone.utc).isoformat()

        if self._is_live_aws:
            try:
                table = self.dynamodb.Table(self.bookings_table_name)
                response = table.update_item(
                    Key={'booking_id': booking_id},
                    UpdateExpression="SET booking_status = :s, payment_status = :p, cancelled_at = :c",
                    ConditionExpression="user_email = :email AND booking_status = :conf",
                    ExpressionAttributeValues={
                        ':s': 'CANCELLED',
                        ':p': 'REFUNDED',
                        ':c': now,
                        ':email': user_email,
                        ':conf': 'CONFIRMED'
                    },
                    ReturnValues="ALL_NEW"
                )
                updated_item = response.get('Attributes')
            except ClientError as e:
                return {"success": False, "error": str(e)}
        else:
            item = self._mock_bookings.get(booking_id)
            if not item or item['user_email'] != user_email:
                return {"success": False, "error": "Booking not found or unauthorized."}
            if item['booking_status'] == 'CANCELLED':
                return {"success": False, "error": "Booking is already cancelled."}
            item['booking_status'] = 'CANCELLED'
            item['payment_status'] = 'REFUNDED'
            item['cancelled_at'] = now
            updated_item = item

        # Real-time cancellation alert via SNS
        self.send_sns_notification(
            subject=f"TravelGo: Booking Cancelled ({booking_id})",
            message=(
                f"Dear Customer,\n\n"
                f"Your booking ({booking_id}) has been CANCELLED successfully.\n\n"
                f"Travel Mode: {updated_item.get('travel_mode', '').upper()}\n"
                f"Route: {updated_item.get('origin', '')} -> {updated_item.get('destination', '')}\n"
                f"Refund Status: Amount will be credited to your original payment method.\n\n"
                f"Regards,\nTravelGo Team"
            )
        )

        return {"success": True, "booking": updated_item}

    def remove_booking(self, booking_id, user_email):
        """Deletes a booking from the database and sends a cancellation notification via SNS."""
        user_email = user_email.strip().lower()

        # Fetch booking details for notification before deletion
        booking_details = None
        if self._is_live_aws:
            try:
                table = self.dynamodb.Table(self.bookings_table_name)
                res = table.get_item(Key={'booking_id': booking_id})
                booking_details = res.get('Item')
                table.delete_item(
                    Key={'booking_id': booking_id},
                    ConditionExpression="user_email = :email",
                    ExpressionAttributeValues={':email': user_email}
                )
            except Exception as e:
                logger.error(f"DynamoDB delete_item error: {e}")
                return {"success": False, "error": str(e)}
        else:
            booking_details = self._mock_bookings.pop(booking_id, None)
            if not booking_details or booking_details.get('user_email') != user_email:
                return {"success": False, "error": "Booking not found or unauthorized."}

        # Send cancellation notification via SNS
        mode = booking_details.get('travel_mode', booking_details.get('type', 'trip')) if booking_details else 'trip'
        self.send_sns_notification(
            subject=f"TravelGo: Booking Removed ({booking_id})",
            message=(
                f"Dear Customer,\n\n"
                f"Your booking record ({booking_id}) for {mode.upper()} has been successfully removed from TravelGo.\n\n"
                f"If you did not initiate this removal, please contact TravelGo support immediately.\n\n"
                f"Regards,\nTravelGo Team"
            )
        )
        return {"success": True, "booking_id": booking_id}

    # -------------------------------------------------------------
    # SNS Notification Service (Scenario 2)
    # -------------------------------------------------------------
    def send_sns_notification(self, subject, message):
        """Dispatches an SNS notification to the configured BookingConfirmation topic."""
        if not self._is_live_aws or not self.sns_topic_arn:
            logger.info(f"[SIMULATED SNS] Subject: {subject}\nMessage:\n{message}")
            return {"success": True, "message_id": f"simulated-sns-{uuid.uuid4().hex[:12]}"}

        try:
            response = self.sns_client.publish(
                TopicArn=self.sns_topic_arn,
                Subject=subject[:100],  # SNS Subject limit is 100 characters
                Message=message
            )
            return {"success": True, "message_id": response.get('MessageId')}
        except Exception as e:
            logger.error(f"SNS publish error: {e}")
            return {"success": False, "error": str(e)}

# Singleton instance
aws_service = AWSService()
