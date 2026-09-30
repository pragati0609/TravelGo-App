from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.aws_service import aws_service

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def index():
    if 'user_email' not in session:
        flash('Please login to view your personal travel dashboard.', 'warning')
        return redirect(url_for('auth.login', next=request.url))

    user_email = session['user_email']
    res = aws_service.get_user_bookings(user_email)
    bookings = res.get('bookings', [])

    # Stats calculation for dynamic dashboard
    total_bookings = len(bookings)
    confirmed_count = sum(1 for b in bookings if b.get('booking_status') == 'CONFIRMED')
    cancelled_count = sum(1 for b in bookings if b.get('booking_status') == 'CANCELLED')
    total_spent = sum(int(b.get('total_amount', 0)) for b in bookings if b.get('booking_status') == 'CONFIRMED')

    active_tab = request.args.get('tab', 'all').lower()

    if active_tab in ('bus', 'train', 'flight', 'hotel'):
        filtered_bookings = [b for b in bookings if b.get('travel_mode') == active_tab]
    else:
        filtered_bookings = bookings

    return render_template(
        'dashboard/index.html',
        bookings=filtered_bookings,
        active_tab=active_tab,
        stats={
            'total': total_bookings,
            'confirmed': confirmed_count,
            'cancelled': cancelled_count,
            'spent': total_spent
        }
    )

@dashboard_bp.route('/cancel-booking/<booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_email' not in session:
        flash('Unauthorized. Please login.', 'danger')
        return redirect(url_for('auth.login'))

    user_email = session['user_email']
    res = aws_service.cancel_booking(booking_id=booking_id, user_email=user_email)

    if res.get('success'):
        flash(f"Booking {booking_id} has been successfully cancelled. A cancellation notice was sent via AWS SNS.", 'success')
    else:
        flash(f"Could not cancel booking: {res.get('error')}", 'danger')

    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/remove-booking/<booking_id>', methods=['GET', 'POST'])
def remove_booking(booking_id):
    """Deletes a booking from DynamoDB and sends a cancellation notification via SNS."""
    if 'user_email' not in session:
        flash('Unauthorized. Please login.', 'danger')
        return redirect(url_for('auth.login'))

    user_email = session['user_email']
    res = aws_service.remove_booking(booking_id=booking_id, user_email=user_email)

    if res.get('success'):
        flash(f"Booking {booking_id} has been permanently removed from database. Notification dispatched via AWS SNS.", 'success')
    else:
        flash(f"Could not remove booking: {res.get('error')}", 'danger')

    return redirect(url_for('dashboard.index'))

