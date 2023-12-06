from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from passlib.hash import sha256_crypt
from email_validator import validate_email, EmailNotValidError

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            emailinfo = validate_email(email, check_deliverability=False)
            email = emailinfo.normalized
        except EmailNotValidError:
            flash("⚠️ Invalid Email. Please enter a valid email.", category='error')
            return render_template("login.html", user=current_user)

        user = User.query.filter_by(email=email).first()
        if user:
            if sha256_crypt.verify(password, user.password):
                flash("🎉 Logged In Successfully! Welcome back!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("❌ Incorrect password, please try again.", category='error')
        else:
            flash("⚠️ Email does not exist. Please check your email or sign up.", category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("👋 You have been logged out. See you again soon!", category='info')
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        try:
            emailinfo = validate_email(email, check_deliverability=True)
            email = emailinfo.normalized
        except EmailNotValidError:
            flash("⚠️ Invalid Email. Please enter a valid email.", category='error')
            return render_template("login.html", user=current_user)

        user = User.query.filter_by(email=email).first()

        if user:
            flash("⚠️ Email already exists. Please use a different email.", category='error')
        elif len(firstName) < 2:
            flash("⚠️ First Name must be greater than 1 character. Please provide a valid name.", category='error')
        elif len(password1) < 7:
            flash("⚠️ Password must be at least 7 characters. Please use a stronger password.", category='error')
        elif password1 != password2:
            flash("⚠️ Passwords don't match. Please make sure the passwords match.", category='error')
        else:
            new_user = User(email=email, first_name=firstName, password=sha256_crypt.hash(password1))
            db.session.add(new_user)
            db.session.commit()
            flash("🎉 Account Created Successfully! Welcome to our community.", category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)