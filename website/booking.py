from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Booking, SERVICES
from . import db

booking = Blueprint('booking', __name__)

@booking.route('/book-appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    if request.method == "POST":
        date = request.form.get('appointmentDate')
        time = request.form.get('appointmentTime')
        service = request.form.get('service')
        price = SERVICES[service]

        new_booking = Booking(date=date, time=time, service=service, price=price, user_id=current_user.id)
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('booking.my_bookings'))
    return render_template("booking.html", user=current_user)

@booking.route('/my-bookings', methods=['GET', 'POST'])
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        booking_id = request.form.get('cancel-booking')
        booking = Booking.query.get(int(booking_id))
        db.session.delete(booking)
        db.session.commit()
        return redirect(url_for('booking.my_bookings'))
    return render_template("my_bookings.html", user=current_user, bookings=bookings)

