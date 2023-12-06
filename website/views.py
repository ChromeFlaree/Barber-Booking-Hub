from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Booking
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if current_user.is_authenticated:
            return redirect(url_for('booking.book_appointment'))
        else:
            flash("⚠️ Please login to book an appointment.", category='error')
            return redirect(url_for('auth.login'))
    return render_template("home.html", user=current_user)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    bookings = current_user.bookings

    if request.method == "POST":
        # check if delete account button was clicked
        if request.form.get('delete-user'):
            # delete all bookings associated with user
            for booking in bookings:
                db.session.delete(booking)
            
            # delete user
            db.session.delete(current_user)
            db.session.commit()
            flash("👋 Your account has been deleted.", category='info')
            return redirect(url_for('auth.login'))
        
        # check if cancel booking button was clicked
        if request.form.get('cancel-booking'):
            booking_id = request.form.get('cancel-booking')
            booking = Booking.query.get(booking_id)
            db.session.delete(booking)
            db.session.commit()
            flash("🗑️ Your appointment has been cancelled!", category='info')
            return redirect(url_for('views.profile'))
        
        # check if edit booking button was clicked
        if request.form.get('update-booking'):
            booking_id = request.form.get('update-booking')
            booking = Booking.query.get(booking_id)
            return redirect(url_for('booking.update_booking', booking_id=booking.id))
        
    return render_template('profile.html', user=current_user, bookings=bookings)