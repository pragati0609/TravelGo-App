import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'travelgo-cloud-booking-secret-key-2026')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')
    
    # AWS Settings
    AWS_REGION = os.environ.get('AWS_REGION', 'ap-south-1')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
    
    # DynamoDB Tables
    USERS_TABLE = os.environ.get('DYNAMODB_USERS_TABLE', 'TravelGo_Users')
    BOOKINGS_TABLE = os.environ.get('DYNAMODB_BOOKINGS_TABLE', 'TravelGo_Bookings')
    
    # SNS
    SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:ap-south-1:123456789012:BookingConfirmation')
    
    # Local Offline Mock Mode (useful for local development before deploying to EC2)
    USE_MOCK_AWS = os.environ.get('USE_MOCK_AWS', 'auto').lower()

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
