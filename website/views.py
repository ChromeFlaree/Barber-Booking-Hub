from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        return redirect(url_for('booking.book_ticket'))
    return render_template("home.html", user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
