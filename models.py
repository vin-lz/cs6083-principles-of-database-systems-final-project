# ------------------------------------------------------------------------------
from flask_login import UserMixin
# ------------------------------------------------------------------------------
from . import db
# ------------------------------------------------------------------------------
from datetime import datetime
# ------------------------------------------------------------------------------


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    pword = db.Column(db.String(45), nullable=False)
    fname = db.Column(db.String(45), nullable=False)
    lname = db.Column(db.String(45), nullable=False)
    street_addr = db.Column(db.String(45), nullable=False)
    cid = db.Column(db.String(45), nullable=False)
    uprofile = db.Column(db.String(280))
    photo = db.Column(db.String(45))
    last_login_timestamp = db.Column(db.DateTime, default=datetime.now())


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(45), nullable=False)
    cstate = db.Column(db.String(45), nullable=False)

class Friendship(db.Model):
    follower = db.Column(db.Integer, primary_key=True)
    followee = db.Column(db.Integer, primary_key=True)
    ftimestamp = db.Column(db.DateTime, default=datetime.now())
    fstatus = db.Column(db.String(45), default='pending')
