from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from services.aws_service import aws_service
# Import custom transport and hotel data from utils.data as required by Epic 1
from utils.data import TRAVEL_CATALOG, BUSES, TRAINS, FLIGHTS, HOTELS

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/', endpoint='home')
@booking_bp.route('/', endpoint='index')
def home():
    """Renders the landing page with the unified multi-mode search widget."""
    return render_template('index.html')

# -----------------------------------------------------------------------------
# Dedicated Transport Routes (Epic 1: separate route handlers for bus, train,
# flight, and hotel search functionalities using POST/GET requests)
# -----------------------------------------------------------------------------
def filter_transport_data(mode_data, mode_name):
    """Filters transport or hotel listings by source/city, destination, and category."""
    origin = (request.form.get('origin') or request.args.get('origin', '')).strip().lower()
    destination = (request.form.get('destination') or request.args.get('destination', '')).strip().lower()
    category = (request.form.get('category') or request.args.get('category', 'all')).lower()
    date = request.form.get('date') or request.args.get('date', datetime.today().strftime('%Y-%m-%d'))

    results = list(mode_data)
    if origin:
        results = [item for item in results if origin in item['origin'].lower()]
    if destination and mode_name != 'hotel':
        results = [item for item in results if destination in item['destination'].lower()]
    if category in ('luxury', 'budget'):
        results = [item for item in results if item.get('category') == category]

    return render_template(
        'booking/search.html',
        results=results,
        mode=mode_name,
        origin=request.form.get('origin') or request.args.get('origin', 'Hyderabad'),
        destination=request.form.get('destination') or request.args.get('destination', 'Bangalore'),
        category=category,
        date=date
    )

@booking_bp.route('/bus', methods=['GET', 'POST'])
def bus_search():
    return filter_transport_data(BUSES, 'bus')

@booking_bp.route('/train', methods=['GET', 'POST'])
def train_search():
    return filter_transport_data(TRAINS, 'train')

@booking_bp.route('/flight', methods=['GET', 'POST'])
def flight_search():
    return filter_transport_data(FLIGHTS, 'flight')

@booking_bp.route('/hotel', methods=['GET', 'POST'])
def hotel_search():
    return filter_transport_data(HOTELS, 'hotel')

# Unified Search Route (supporting GET and POST)
@booking_bp.route('/search', methods=['GET', 'POST'])
def search():
    mode = (request.form.get('mode') or request.args.get('mode', 'bus')).lower()
    if mode == 'bus':
        return filter_transport_data(BUSES, 'bus')
    elif mode == 'train':
        return filter_transport_data(TRAINS, 'train')
    elif mode == 'flight':
        return filter_transport_data(FLIGHTS, 'flight')
    elif mode == 'hotel':
        return filter_transport_data(HOTELS, 'hotel')
    return filter_transport_data(TRAVEL_CATALOG, 'bus')

# -----------------------------------------------------------------------------
# Seat Selection Route (Epic 1: seat selecting routes for bus page)
# -----------------------------------------------------------------------------
@booking_bp.route('/select-seats/<listing_id>')
@booking_bp.route('/bus-seats/<listing_id>')
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

# -----------------------------------------------------------------------------
# Booking Route (Epic 1: Saves booking details in session and redirects to payment)
# -----------------------------------------------------------------------------
@booking_bp.route('/book', methods=['POST'])
def book():
    if 'user_email' not in session:
        flash('Session expired or not logged in. Please login to complete booking.', 'warning')
        return redirect(url_for('auth.login'))

    listing_id = request.form.get('listing_id')
    listing = next((item for item in TRAVEL_CATALOG if item['id'] == listing_id), None)

    travel_mode = request.form.get('travel_mode', listing['travel_mode'] if listing else 'bus')
    origin = request.form.get('origin', listing['origin'] if listing else 'Hyderabad')
    destination = request.form.get('destination', listing['destination'] if listing else 'Bangalore')
    travel_date = request.form.get('travel_date', datetime.today().strftime('%Y-%m-%d'))
    seat_numbers = request.form.get('seat_numbers', '')
    room_preference = request.form.get('room_preference', '')
    provider_name = request.form.get('provider_name', listing['provider_name'] if listing else 'TravelGo Express')

    total_amount = int(request.form.get('total_amount', 0))
    if not total_amount and listing:
        total_amount = listing['total_amount']

    # Package pending booking data
    pending_booking = {
        'listing_id': listing_id,
        'travel_mode': travel_mode,
        'provider_name': provider_name,
        'origin': origin,
        'destination': destination,
        'travel_date': travel_date,
        'seat_numbers': seat_numbers,
        'room_preference': room_preference,
        'total_amount': total_amount,
        'departure_time': listing.get('departure_time', '10:00 AM') if listing else '10:00 AM',
        'arrival_time': listing.get('arrival_time', '06:00 PM') if listing else '06:00 PM'
    }

    # Store in session as required by Epic 1 specification
    session['pending_booking'] = pending_booking

    # If payment_method is directly supplied in form or direct payment requested
    payment_method = request.form.get('payment_method')
    if payment_method or request.form.get('skip_payment') == 'true' or request.headers.get('X-Direct-Book') == 'true':
        pending_booking['payment_method'] = payment_method or 'Credit Card / UPI'
        res = aws_service.create_booking(user_email=user_email, booking_data=pending_booking)
        if res.get('success'):
            booking = res['booking']
            session.pop('pending_booking', None)
            flash(f"Booking {booking['booking_id']} confirmed! Real-time alert dispatched via AWS SNS.", 'success')
            return redirect(url_for('booking.confirmation', booking_id=booking['booking_id']))

    # Otherwise redirect to the payment checkout page as per Epic 1 specification
    return redirect(url_for('booking.payment'))

# -----------------------------------------------------------------------------
# Payment Route (Epic 1: Processes payment details, stores booking in database,
# sends SNS confirmation notification, then redirects to dashboard)
# -----------------------------------------------------------------------------
@booking_bp.route('/payment', methods=['GET', 'POST'])
def payment():
    if 'user_email' not in session:
        flash('Please login to complete your payment.', 'warning')
        return redirect(url_for('auth.login'))

    pending_booking = session.get('pending_booking')
    if not pending_booking:
        flash('No pending booking found. Please select your travel first.', 'info')
        return redirect(url_for('booking.home'))

    if request.method == 'GET':
        return render_template('booking/payment.html', booking=pending_booking)

    # POST: Process Payment
    user_email = session['user_email']
    payment_method = request.form.get('payment_method', 'Credit Card / UPI')
    pending_booking['payment_method'] = payment_method

    # Save booking to DynamoDB & dispatch SNS confirmation
    res = aws_service.create_booking(user_email=user_email, booking_data=pending_booking)

    if res.get('success'):
        booking = res['booking']
        session.pop('pending_booking', None)
        flash(f"Payment successful! Booking {booking['booking_id']} confirmed. Real-time alert dispatched via AWS SNS.", 'success')
        return redirect(url_for('dashboard.index'))
    else:
        flash(f"Payment or booking failed: {res.get('error')}", 'danger')
        return redirect(url_for('booking.payment'))

@booking_bp.route('/payment-process')
def payment_process():
    """Direct payment execution helper."""
    if 'user_email' not in session or 'pending_booking' not in session:
        return redirect(url_for('booking.home'))
    user_email = session['user_email']
    pending_booking = session.pop('pending_booking')
    res = aws_service.create_booking(user_email=user_email, booking_data=pending_booking)
    if res.get('success'):
        booking = res['booking']
        flash('Booking confirmed! AWS SNS notification sent.', 'success')
        return redirect(url_for('booking.confirmation', booking_id=booking['booking_id']))
    return redirect(url_for('booking.home'))

@booking_bp.route('/booking-confirmation/<booking_id>')
def confirmation(booking_id):
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))

    user_email = session['user_email']
    bookings_res = aws_service.get_user_bookings(user_email)
    booking = next((b for b in bookings_res.get('bookings', []) if b['booking_id'] == booking_id), None)

    if not booking:
        flash('Booking record confirmed.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('booking/confirmation.html', booking=booking)
