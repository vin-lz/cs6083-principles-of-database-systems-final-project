# ------------------------------------------------------------------------------
from flask_login import UserMixin
# ------------------------------------------------------------------------------
from . import db
# ------------------------------------------------------------------------------
from datetime import datetime
# ------------------------------------------------------------------------------


class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(45), unique=True, nullable=False)
    pword = db.Column(db.String(45), nullable=False)
    fname = db.Column(db.String(45), nullable=False)
    lname = db.Column(db.String(45), nullable=False)
    street_addr = db.Column(db.String(45), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey('City.id'), nullable=False)
    uprofile = db.Column(db.Text)
    photo = db.Column(db.Text)
    last_login_timestamp = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))


class City(db.Model):
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(45), nullable=False)
    cstate = db.Column(db.String(45), nullable=False)


class Friendship(db.Model):
    __tablename__ = 'Friendship'
    follower = db.Column(db.Integer, db.ForeignKey(
        'Users.id'), primary_key=True)
    followee = db.Column(db.Integer, db.ForeignKey(
        'Users.id'), primary_key=True)
    ftimestamp = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))
    fstatus = db.Column(db.String(45), default='pending')


class Neighboring(db.Model):
    __tablename__ = 'Neighboring'
    initiator = db.Column(db.Integer, db.ForeignKey(
        'Users.id'), primary_key=True)
    acceptor = db.Column(db.Integer, db.ForeignKey(
        'Users.id'), primary_key=True)
    ntimestamp = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0))


class Hood(db.Model):
    __tablename__ = 'Hood'
    id = db.Column(db.Integer, primary_key=True)
    hname = db.Column(db.String(45), nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    hpopulation = db.Column(db.Integer, nullable=False)


class Blocks(db.Model):
    __tablename__ = 'Blocks'
    id = db.Column(db.Integer, primary_key=True)
    bname = db.Column(db.String(45), nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    sw_lat = db.Column(db.Float, nullable=False)
    bpopulation = db.Column(db.Integer, nullable=False)


class Location(db.Model):
    __tablename__ = 'Location'
    bid = db.Column(db.Integer, primary_key=True)
    hid = db.Column(db.Integer, db.ForeignKey('Hood.id'), primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('City.id'), primary_key=True)


class Membership(db.Model):
    __tablename__ = 'Membership'
    uid = db.Column(db.Integer, db.ForeignKey('Users.id'),
                    nullable=False, primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey('Blocks.id'),
                    nullable=False, primary_key=True)
    approval_count = db.Column(db.Integer, nullable=False, default=0)


class Approval(db.Model):
    __tablename__ = 'Approval'
    approver = db.Column(db.Integer, db.ForeignKey(
        'Users.id'), primary_key=True)
    approvee = db.Column(db.Integer, db.ForeignKey(
        'Membership.uid'), primary_key=True)
    bid = db.Column(db.Integer, db.ForeignKey('Blocks.id'), primary_key=True)


class Message(db.Model):
    __tablename__ = 'Message'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    mtimestamp = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0), nullable=False)
    visibility = db.Column(db.String(45), nullable=False)
    receiver = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)


class Reply(db.Model):
    __tablename__ = 'Reply'
    id = db.Column(db.Integer, primary_key=True)
    mid = db.Column(db.Integer, db.ForeignKey('Message.id'), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rtimestamp = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0), nullable=False)


class Thread(db.Model):
    __tablename__ = 'Thread'
    uid = db.Column(db.Integer, db.ForeignKey('Users.id'),
                    nullable=False, primary_key=True)
    mid = db.Column(db.Integer, db.ForeignKey('Message.id'),
                    nullable=False, primary_key=True)
    tstatus = db.Column(db.String(45), nullable=False, default='unread')
    ttimestamp = db.Column(db.DateTime, default=datetime.now().replace(microsecond=0), nullable=False)