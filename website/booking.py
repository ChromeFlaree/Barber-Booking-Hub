from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Booking, SERVICES
from . import db

booking = Blueprint('booking', __name__)

@booking.route('/book-appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == "POST":
        date = request.form.get('appointmentDate')
        if len(date) == 0:
            flash("⚠️ Date cannot be empty. Please enter a valid date.", category='error')
            return render_template("booking.html", user=current_user)

        time = request.form.get('appointmentTime')
        if len(time) == 0:
            flash("⚠️ Time cannot be empty. Please enter a valid time.", category='error')
            return render_template("booking.html", user=current_user)

        service = request.form.get('service')
        price = SERVICES[service]

        new_booking = Booking(date=date, time=time, service=service, price=price, user_id=current_user.id)
        db.session.add(new_booking)
        db.session.commit()

        flash("🎉 Your appointment has been booked!", category='success')
        return redirect(url_for('views.profile'))

    return render_template("booking.html", user=current_user)

@booking.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        booking_id = request.form.get('cancel-booking')
        if booking_id:
            booking = Booking.query.get(int(booking_id))
            db.session.delete(booking)
            db.session.commit()
            flash("👍 Your appointment has been cancelled!", category='success')
            return redirect(url_for('booking.profile'))

    return render_template('profile.html', user=current_user, bookings=bookings)