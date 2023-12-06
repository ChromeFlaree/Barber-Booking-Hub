from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user

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

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
