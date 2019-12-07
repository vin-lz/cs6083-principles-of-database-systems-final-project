# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, redirect, url_for, request, flash
# ------------------------------------------------------------------------------
from werkzeug.security import generate_password_hash, check_password_hash
# ------------------------------------------------------------------------------
from flask_login import login_user, logout_user, login_required, current_user
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
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.pword, password):
        flash('Please check your login credentials and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('auth.account'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')
    street_address = request.form.get('street-address')
    city_name = request.form.get('city')
    city_state = request.form.get('state')

    # if this returns a user, then the email already exists in database
    user = Users.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists, please try login')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.

    if email and first_name and last_name and new_password and confirm_password and street_address and city_name and city_state:
        # Passwords dismatch
        if new_password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('auth.signup'))
        else:
            city = City.query.filter_by(cname=city_name, cstate=city_state).first()
            # City found
            if city:
                city_id = city.id
            # Need new city
            else:
                new_city = City(cname=city_name, cstate=city_state)
                db.session.add(new_city)
                db.session.commit()
                city_id = City.query.filter_by(
                cname=city_name, cstate=city_state).first().id

                new_user = Users(email=email, fname=first_name, lname=last_name, pword=generate_password_hash(
                new_password, method='sha256'), street_addr=street_address, cid=city_id, last_login_timestamp=datetime.now())

                # add the new user to the database
                db.session.add(new_user)
                db.session.commit()
        # Successful!
        return redirect(url_for('auth.login'))
        # Missing info!
    else:
        flash('Missing mandatory infomation')
        return redirect(url_for('auth.signup'))

@auth.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@auth.route('/account', methods=['POST'])
@login_required
def account_post():
    street_address = request.form.get('street-address')
    if street_address and street_address.replace(' ',''):
        Users.query.filter_by(id=current_user.id).first().street_addr=street_address
        db.session.commit()
    else:
        flash('Street cannot be empty')
        return redirect(url_for('auth.account'))

    profile = request.form.get('profile')
    if profile != current_user.uprofile and profile:
        Users.query.filter_by(id=current_user.id).first().uprofile = profile
        db.session.commit()

    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')
    if new_password or confirm_password:
        if new_password==confirm_password:
            Users.query.filter_by(id=current_user.id).first().pword = generate_password_hash(new_password, method='sha256')
            db.session.commit()
        else:
            flash('Passwords do not match')
            return redirect(url_for('auth.account'))
    flash('Save successfully')
    return redirect(url_for('auth.account'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))