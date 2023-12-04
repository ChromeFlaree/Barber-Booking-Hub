from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .services import get_user_info 

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
    user_info = get_user_info(current_user.id)
    return render_template('profile.html', user_info=user_info, user=current_user)
