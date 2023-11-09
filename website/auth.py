from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from passlib.hash import sha256_crypt

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if sha256_crypt.verify(password, user.password):
                flash("Logged in successfully!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password, try again", category='error')
        else:
            flash("Email does not exist", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists", category='error')
        elif len(email) == 0:
            flash("Email can't be empty", category='error')
        elif len(firstName) < 2:
            flash("First Name must be greater than 1 character", category='error')
        elif len(password1) < 7:
            flash("Password must be atleast 7 characters", category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=sha256_crypt.hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)