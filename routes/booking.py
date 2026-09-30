from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.aws_service import aws_service
from datetime import datetime

booking_bp = Blueprint('booking', __name__)

# Mock catalog of realistic travel options (Hyderabad <-> Bangalore, Chennai, Mumbai, Delhi)
TRAVEL_CATALOG = [
    # Buses
    {
        'id': 'BUS-01',
        'mode': 'bus',
        'provider': 'Orange Travels Multi-Axle Volvo',
        'type': 'AC Sleeper / Seater (2+1)',
        'origin': 'Hyderabad',
        'destination': 'Bangalore',
        'departure': '21:30',
        'arrival': '06:00',
        'duration': '8h 30m',
        'price': 1200,
        'rating': 4.8,
        'category': 'luxury',
        'total_seats': 30
    },
    {
        'id': 'BUS-02',
        'mode': 'bus',
        'provider': 'KSRTC Airavat Club Class',
        'type': 'Multi-Axle Semi-Sleeper',
        'origin': 'Hyderabad',
        'destination': 'Bangalore',
        'departure': '22:15',
        'arrival': '06:45',
        'duration': '8h 30m',
        'price': 950,
        'rating': 4.6,
        'category': 'budget',
        'total_seats': 36
    },
    {
        'id': 'BUS-03',
        'mode': 'bus',
        'provider': 'SRS Travels Volvo B11R',
        'type': 'Multi-Axle AC Sleeper',
        'origin': 'Chennai',
        'destination': 'Bangalore',
        'departure': '23:00',
        'arrival': '05:30',
        'duration': '6h 30m',
        'price': 850,
        'rating': 4.5,
        'category': 'budget',
        'total_seats': 30
    },
    # Trains
    {
        'id': 'TRN-101',
        'mode': 'train',
        'provider': 'Vande Bharat Express (20608)',
        'type': 'Executive AC Chair Car',
        'origin': 'Hyderabad',
        'destination': 'Bangalore',
        'departure': '06:00',
        'arrival': '14:30',
        'duration': '8h 30m',
        'price': 1850,
        'rating': 4.9,
        'category': 'luxury'
    },
    {
        'id': 'TRN-102',
        'mode': 'train',
        'provider': 'Kacheguda Express (12785)',
        'type': '3rd AC Economy (3A)',
        'origin': 'Hyderabad',
        'destination': 'Bangalore',
        'departure': '19:05',
        'arrival': '06:25',
        'duration': '11h 20m',
        'price': 890,
        'rating': 4.3,
        'category': 'budget'
    },
    # Flights
    {
        'id': 'FLT-501',
        'mode': 'flight',
        'provider': 'IndiGo (6E-6421)',
        'type': 'Airbus A321 Neo',
        'origin': 'Hyderabad',
        'destination': 'Bangalore',
        'departure': '08:45',
        'arrival': '09:55',
        'duration': '1h 10m',
        'price': 3499,
        'rating': 4.7,
        'category': 'budget'
    },
    {
        'id': 'FLT-502',
        'mode': 'flight',
        'provider': 'Air India (AI-512)',
        'type': 'Boeing 787 Dreamliner (Business)',
        'origin': 'Hyderabad',
        'destination': 'Bangalore',
        'departure': '17:15',
        'arrival': '18:30',
        'duration': '1h 15m',
        'price': 8999,
        'rating': 4.8,
        'category': 'luxury'
    },
    # Hotels
    {
        'id': 'HTL-901',
        'mode': 'hotel',
        'provider': 'Taj Bangalore Airport Residency',
        'type': 'Luxury Deluxe Suite with Breakfast',
        'origin': 'Bangalore',
        'destination': 'Bangalore',
        'departure': '14:00 (Check-in)',
        'arrival': '12:00 (Check-out)',
        'duration': '1 Night',
        'price': 7500,
        'rating': 4.9,
        'category': 'luxury'
    },
    {
        'id': 'HTL-902',
        'mode': 'hotel',
        'provider': 'Ginger Hotel Whitefield',
        'type': 'Standard Executive Smart Room',
        'origin': 'Bangalore',
        'destination': 'Bangalore',
        'departure': '12:00 (Check-in)',
        'arrival': '11:00 (Check-out)',
        'duration': '1 Night',
        'price': 2200,
        'rating': 4.2,
        'category': 'budget'
    },
    {
        'id': 'HTL-903',
        'mode': 'hotel',
        'provider': 'The Leela Palace Chennai',
        'type': 'Sea View Royal Luxury Room',
        'origin': 'Chennai',
        'destination': 'Chennai',
        'departure': '14:00 (Check-in)',
        'arrival': '12:00 (Check-out)',
        'duration': '1 Night',
        'price': 9800,
        'rating': 5.0,
        'category': 'luxury'
    },
    {
        'id': 'HTL-904',
        'mode': 'hotel',
        'provider': 'Ibis City Centre',
        'type': 'Budget Cosy Double Room',
        'origin': 'Chennai',
        'destination': 'Chennai',
        'departure': '13:00 (Check-in)',
        'arrival': '11:00 (Check-out)',
        'duration': '1 Night',
        'price': 2800,
        'rating': 4.4,
        'category': 'budget'
    }
]

@booking_bp.route('/')
def index():
    return render_template('index.html')

@booking_bp.route('/search')
def search():
    mode = request.args.get('mode', 'bus').lower()
    origin = request.args.get('origin', '').strip().lower()
    destination = request.args.get('destination', '').strip().lower()
    category = request.args.get('category', 'all').lower()
    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))

    results = [item for item in TRAVEL_CATALOG if item['mode'] == mode]

    if origin:
        results = [item for item in results if origin in item['origin'].lower()]
    if destination and mode != 'hotel':
        results = [item for item in results if destination in item['destination'].lower()]
    if category in ('luxury', 'budget'):
        results = [item for item in results if item.get('category') == category]

    return render_template(
        'booking/search.html',
        results=results,
        mode=mode,
        origin=request.args.get('origin', 'Hyderabad'),
        destination=request.args.get('destination', 'Bangalore'),
        category=category,
        date=date
    )

@booking_bp.route('/select-seats/<listing_id>')
def select_seats(listing_id):
    if 'user_email' not in session:
        flash('Please login to select seats and book your travel.', 'warning')
        return redirect(url_for('auth.login', next=request.url))

    listing = next((item for item in TRAVEL_CATALOG if item['id'] == listing_id), None)
    if not listing:
        flash('Listing not found.', 'danger')
        return redirect(url_for('booking.search'))

    date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    return render_template('booking/bus_seats.html', listing=listing, date=date)

@booking_bp.route('/book', methods=['POST'])
def book():
    if 'user_email' not in session:
        flash('Session expired. Please login to complete booking.', 'warning')
        return redirect(url_for('auth.login'))

    user_email = session['user_email']
    listing_id = request.form.get('listing_id')
    listing = next((item for item in TRAVEL_CATALOG if item['id'] == listing_id), None)

    travel_mode = request.form.get('travel_mode', 'bus')
    origin = request.form.get('origin', 'Hyderabad')
    destination = request.form.get('destination', 'Bangalore')
    travel_date = request.form.get('travel_date', datetime.today().strftime('%Y-%m-%d'))
    seat_numbers = request.form.get('seat_numbers', '')
    room_preference = request.form.get('room_preference', '')
    provider_name = request.form.get('provider_name', listing['provider'] if listing else 'TravelGo')

    # Calculate total amount
    total_amount = int(request.form.get('total_amount', 0))
    if not total_amount and listing:
        total_amount = listing['price']

    booking_data = {
        'travel_mode': travel_mode,
        'provider_name': provider_name,
        'origin': origin,
        'destination': destination,
        'travel_date': travel_date,
        'seat_numbers': seat_numbers,
        'room_preference': room_preference,
        'total_amount': total_amount,
        'departure_time': listing['departure'] if listing else '10:00 AM',
        'arrival_time': listing['arrival'] if listing else '06:00 PM'
    }

    res = aws_service.create_booking(user_email=user_email, booking_data=booking_data)
    if res.get('success'):
        booking = res['booking']
        flash('Booking confirmed! A real-time notification has been sent via AWS SNS.', 'success')
        return redirect(url_for('booking.confirmation', booking_id=booking['booking_id']))
    else:
        flash(f"Booking failed: {res.get('error')}", 'danger')
        return redirect(url_for('booking.search', mode=travel_mode))

@booking_bp.route('/booking-confirmation/<booking_id>')
def confirmation(booking_id):
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))

    # Fetch booking from user history
    user_email = session['user_email']
    bookings_res = aws_service.get_user_bookings(user_email)
    booking = next((b for b in bookings_res.get('bookings', []) if b['booking_id'] == booking_id), None)

    if not booking:
        flash('Booking not found.', 'danger')
        return redirect(url_for('dashboard.index'))

    return render_template('booking/confirmation.html', booking=booking)
