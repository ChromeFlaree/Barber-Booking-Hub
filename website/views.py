from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from website.booking import cancel_booking
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # check if user is logged in
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
            return cancel_booking(booking_id)          
        
        # check if edit booking button was clicked
        if request.form.get('update-booking'):
            booking_id = request.form.get('update-booking')
            return redirect(url_for('booking.update_booking', booking_id=booking_id))
        
    return render_template('profile.html', user=current_user, bookings=bookings)