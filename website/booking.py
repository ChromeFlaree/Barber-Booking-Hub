from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import delete
from .models import Booking
from . import db

booking = Blueprint('booking', __name__)

@booking.route('/book-ticket', methods=['GET', 'POST'])
@login_required
def book_ticket():
    if request.method == "POST":
        date = request.form.get('date')
        time = request.form.get('time')
        service = request.form.get('service')

        new_booking = Booking(date=date, time=time, service=service, user_id=current_user.id)
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('booking.my_bookings'))
    return render_template("booking.html", user=current_user)

@booking.route('/my-bookings', methods=['GET', 'POST'])
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template("my_bookings.html", user=current_user, bookings=bookings)

@booking.route('/delete-booking/<int:id>')
@login_required
def delete_booking(id):
    booking = Booking.query.filter_by(id=id).first()
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('booking.my_bookings'))
