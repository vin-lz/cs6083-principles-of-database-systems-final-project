# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, redirect, url_for, request, flash
# ------------------------------------------------------------------------------
from werkzeug.security import generate_password_hash, check_password_hash
# ------------------------------------------------------------------------------
from flask_login import login_user, logout_user, login_required
# ------------------------------------------------------------------------------
from datetime import datetime
# ------------------------------------------------------------------------------
from . import db
from .models import Users
from .models import City
# ------------------------------------------------------------------------------

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    pword = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.pword, pword):
        flash('Please check your login credentials and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.account'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    fname = request.form.get('first-name')
    lname = request.form.get('last-name')
    pword = request.form.get('password')
    street_addr = request.form.get('street-address')
    cname = request.form.get('city')
    cstate = request.form.get('state')

    # if this returns a user, then the email already exists in database
    user = Users.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    city = City.query.filter_by(cname=cname, cstate=cstate).first()
    if city:
        cid = city.id
    else:
        new_city = City(cname=cname, cstate=cstate)
        db.session.add(new_city)
        db.session.commit()
        cid = City.query.filter_by(cname=cname, cstate=cstate).first().id

    new_user = Users(email=email, fname=fname, lname=lname, pword=generate_password_hash(
        pword, method='sha256'), street_addr=street_addr, cid=cid, last_login_timestamp=datetime.now())

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
