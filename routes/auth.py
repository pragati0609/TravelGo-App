from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.aws_service import aws_service

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash('Please fill out all required fields.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        res = aws_service.register_user(email=email, password=password, full_name=full_name, phone=phone)
        if res.get('success'):
            flash('Registration successful! Please login to continue.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash(res.get('error', 'Registration failed.'), 'danger')
            return render_template('auth/register.html')

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please provide both email and password.', 'warning')
            return render_template('auth/login.html')

        res = aws_service.authenticate_user(email=email, password=password)
        if res.get('success'):
            user = res['user']
            session['user_email'] = user['email']
            session['user_name'] = user['full_name']
            session['user_role'] = user.get('role', 'user')
            flash(f"Welcome back, {user['full_name']}!", 'success')
            next_url = request.args.get('next') or url_for('dashboard.index')
            return redirect(next_url)
        else:
            flash(res.get('error', 'Invalid login credentials.'), 'danger')
            return render_template('auth/login.html')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('booking.index'))
