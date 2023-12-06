from . import db
from flask_login import UserMixin

SERVICES = {
    "Haircut": 25,
    "Beard Trim": 15,
    "Shave": 20,
    "Haircut & Beard Trim": 35,
    "Haircut & Shave": 40
}


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    image = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    bookings = db.relationship('Booking')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    time = db.Column(db.String(5))
    service = db.Column(db.String(150))
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
