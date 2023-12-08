from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Appointment, SERVICES
from . import db
from datetime import datetime

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
        
        # check if date and time is in the past
        booking_datetime = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
        if booking_datetime < datetime.now():
            flash("⚠️ You cannot book an appointment in the past.", category='error')
            return render_template("booking.html", user=current_user)
        
        # check if date and time is already taken
        booking = Appointment.query.filter_by(date=date, time=time, user_id=current_user.id).first()
        if booking:
            flash("⚠️ You already have an appointment at this time.", category='error')
            return render_template("booking.html", user=current_user)

        service = request.form.get('service')
        price = SERVICES[service]

        new_booking = Appointment(date=date, time=time, service=service, price=price, user_id=current_user.id)
        db.session.add(new_booking)
        db.session.commit()

        flash("🎉 Your appointment has been booked!", category='success')
        return redirect(url_for('views.profile'))

    return render_template("booking.html", user=current_user)


@booking.route('/update-booking/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def update_booking(booking_id):
    booking = Appointment.query.get(booking_id)

    if request.method == "POST":
        date = request.form.get('appointmentDate')
        time = request.form.get('appointmentTime')
        
        # check if new date and time is in the past
        booking_datetime = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
        if booking_datetime < datetime.now():
            flash("⚠️ You cannot book an appointment in the past.", category='error')
            return render_template("update_booking.html", user=current_user, booking=booking)
        
        # check if same appointment already exists
        service = request.form.get('service')
        booking_check = Appointment.query.filter_by(date=date, time=time, service=service, user_id=current_user.id).first()
        if booking_check:
            flash("⚠️ You already have a same appointment at this time.", category='error')
            return render_template("update_booking.html", user=current_user, booking=booking)
        
        booking.date = date
        booking.time = time
        booking.service = service
        booking.price = SERVICES[booking.service]
        
        db.session.commit()
        flash("🎉 Your appointment has been updated!", category='success')
        return redirect(url_for('views.profile'))

    return render_template("update_booking.html", user=current_user, booking=booking)

def cancel_booking(booking_id):
    booking = Appointment.query.get(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash("🗑️ Your appointment has been cancelled!", category='info')
    return redirect(url_for('views.profile'))