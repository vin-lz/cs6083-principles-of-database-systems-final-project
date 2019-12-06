# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, request, flash, redirect, url_for
# ------------------------------------------------------------------------------
from flask_login import login_required, current_user
# ------------------------------------------------------------------------------
from . import db
from .models import Users
from .models import City
# ------------------------------------------------------------------------------
from werkzeug.security import generate_password_hash

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/account')
@login_required
def account():
    return render_template('account.html', user=current_user)

@main.route('/account', methods=['POST'])
@login_required
def account_post():
    street_address = request.form.get('street-address')
    if street_address and street_address.replace(' ',''):
        Users.query.filter_by(id=current_user.id).first().street_addr=street_address
        db.session.commit()
    else:
        flash('Street cannot be empty')
        return redirect(url_for('main.account'))

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
            return redirect(url_for('main.account'))
    flash('Save successfully')
    return render_template('account.html', user=current_user)
