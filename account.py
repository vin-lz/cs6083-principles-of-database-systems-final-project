# ------------------------------------------------------------------------------
from flask import Blueprint, render_template, redirect, url_for, request, flash
# ------------------------------------------------------------------------------
from werkzeug.security import generate_password_hash, check_password_hash
# ------------------------------------------------------------------------------
from flask_login import login_user, logout_user, login_required, current_user
# ------------------------------------------------------------------------------
from . import db
from .models import Users
from .models import City
from .models import Blocks
from .models import Hood
from .models import Membership
from .models import Location
# ------------------------------------------------------------------------------
from datetime import datetime
# ------------------------------------------------------------------------------

acc = Blueprint('acc', __name__)


@acc.route('/account')
@login_required
def account():
    city = City.query.filter_by(id=current_user.cid).first()
    if Membership.query.filter_by(uid=current_user.id).first():
        block_name = Blocks.query.filter_by(
            id=(Membership.query.filter_by(uid=current_user.id).first().bid)).first().bname
        hood_name = Hood.query.filter_by(id=(Location.query.filter_by(bid=(Blocks.query.filter_by(id=(Membership.query.filter_by(
            uid=current_user.id).first().bid)).first().id), cid=current_user.cid).first().hid)).first().hname

        return render_template('account.html', user=current_user, city=city, block='%s, %s' % (block_name, hood_name))
    else:

        return render_template('account.html', user=current_user, city=city, block='You haven\'t joined any block.')


@acc.route('/account', methods=['POST'])
@login_required
def account_info_post():
    street_address = request.form.get('street-address')
    if street_address and street_address.replace(' ', ''):
        Users.query.filter_by(
            id=current_user.id).first().street_addr = street_address
        db.session.commit()
    else:
        flash('Street cannot be empty')
        return redirect(url_for('acc.account'))

    profile = request.form.get('profile')
    if profile != current_user.uprofile and profile:
        Users.query.filter_by(id=current_user.id).first().uprofile = profile
        db.session.commit()

    new_password = request.form.get('new-password')
    confirm_password = request.form.get('confirm-password')
    if new_password or confirm_password:
        if new_password == confirm_password:
            Users.query.filter_by(id=current_user.id).first(
            ).pword = generate_password_hash(new_password, method='sha256')
            db.session.commit()
        else:
            flash('Passwords do not match')
            return redirect(url_for('acc.account'))
    flash('Save successfully')
    return redirect(url_for('acc.account'))
