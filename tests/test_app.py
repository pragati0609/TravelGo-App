# Task 17: Functional Tests for TravelGo
# Tests run entirely in-memory using the built-in mock mode (no real AWS credentials needed)
# Usage: python -m pytest tests/ -v --tb=short

import pytest
import sys
import os

# Ensure parent dir is on path so 'app' can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app


@pytest.fixture
def client():
    """Create a test client for TravelGo with mock AWS mode."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client


# ─── Helper ──────────────────────────────────────────────────────────────────

def register_and_login(client, email='test@travelgo.in', name='Test User', password='Test@1234'):
    """Register a user and then log them in. Returns response of login."""
    client.post('/auth/register', data={
        'full_name': name,
        'email': email,
        'password': password,
        'confirm_password': password
    }, follow_redirects=True)
    return client.post('/auth/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)


# ─── Scenario 0: Home Page ───────────────────────────────────────────────────

class TestHomePage:
    def test_home_returns_200(self, client):
        resp = client.get('/')
        assert resp.status_code == 200

    def test_home_contains_travelgo(self, client):
        resp = client.get('/')
        assert b'TravelGo' in resp.data


# ─── Scenario 1: User Authentication ─────────────────────────────────────────

class TestAuthentication:
    def test_register_get(self, client):
        resp = client.get('/auth/register')
        assert resp.status_code == 200

    def test_register_new_user(self, client):
        resp = client.post('/auth/register', data={
            'full_name': 'Priya Sharma',
            'email': 'priya@travelgo.in',
            'password': 'Secure@123',
            'confirm_password': 'Secure@123'
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Registration successful' in resp.data or b'login' in resp.data.lower()

    def test_login_valid_credentials(self, client):
        register_and_login(client)
        resp = client.get('/dashboard')
        assert resp.status_code == 200

    def test_login_invalid_password(self, client):
        client.post('/auth/register', data={
            'full_name': 'Ravi Kumar',
            'email': 'ravi@travelgo.in',
            'password': 'Right@123',
            'confirm_password': 'Right@123'
        }, follow_redirects=True)
        resp = client.post('/auth/login', data={
            'email': 'ravi@travelgo.in',
            'password': 'Wrong@999'
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b'Invalid' in resp.data

    def test_logout_clears_session(self, client):
        register_and_login(client)
        resp = client.get('/auth/logout', follow_redirects=True)
        assert resp.status_code == 200
        # After logout, dashboard should redirect to login
        resp2 = client.get('/dashboard', follow_redirects=True)
        assert b'Login' in resp2.data or b'login' in resp2.data.lower()


# ─── Scenario 2: Multi-Mode Search & Booking ─────────────────────────────────

class TestBookingFlow:
    def test_search_bus(self, client):
        register_and_login(client)
        resp = client.get('/search?mode=bus')
        assert resp.status_code == 200
        assert b'bus' in resp.data.lower() or b'Bus' in resp.data

    def test_search_train(self, client):
        register_and_login(client)
        resp = client.get('/search?mode=train')
        assert resp.status_code == 200

    def test_search_flight(self, client):
        register_and_login(client)
        resp = client.get('/search?mode=flight')
        assert resp.status_code == 200

    def test_search_hotel_luxury_filter(self, client):
        register_and_login(client)
        resp = client.get('/search?mode=hotel&category=luxury')
        assert resp.status_code == 200

    def test_bus_seat_selection_page(self, client):
        register_and_login(client)
        resp = client.get('/select-seats/BUS-01')
        assert resp.status_code == 200
        assert b'seat' in resp.data.lower()

    def test_complete_bus_booking(self, client):
        register_and_login(client)
        resp = client.post('/book', data={
            'listing_id': 'BUS-01',
            'travel_date': '2025-12-20',
            'seat_numbers': '2A,3A'
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b'BK-' in resp.data  # Booking ID format

    def test_complete_hotel_booking(self, client):
        register_and_login(client)
        resp = client.post('/book', data={
            'listing_id': 'HTL-01',
            'travel_date': '2025-12-25',
            'num_guests': '2'
        }, follow_redirects=True)
        assert resp.status_code == 200
        assert b'BK-' in resp.data


# ─── Scenario 3: Dashboard & Cancellation ────────────────────────────────────

class TestDashboard:
    def test_dashboard_shows_booking(self, client):
        register_and_login(client)
        client.post('/book', data={
            'listing_id': 'TRN-01',
            'travel_date': '2025-12-22',
        }, follow_redirects=True)
        resp = client.get('/dashboard')
        assert resp.status_code == 200
        assert b'CONFIRMED' in resp.data or b'Confirmed' in resp.data

    def test_cancellation_changes_status(self, client):
        register_and_login(client)
        # Create a booking
        book_resp = client.post('/book', data={
            'listing_id': 'FLT-01',
            'travel_date': '2025-12-25',
        }, follow_redirects=True)
        # Extract booking_id from confirmation page
        import re
        booking_ids = re.findall(rb'BK-[A-Z0-9]+', book_resp.data)
        assert booking_ids, "No booking ID found in confirmation page"
        bid = booking_ids[0].decode()
        # Cancel it
        resp = client.post(f'/cancel-booking/{bid}', follow_redirects=True)
        assert resp.status_code == 200
        assert b'Cancelled' in resp.data or b'CANCELLED' in resp.data

    def test_dashboard_tab_filter(self, client):
        register_and_login(client)
        resp = client.get('/dashboard?tab=bus')
        assert resp.status_code == 200
