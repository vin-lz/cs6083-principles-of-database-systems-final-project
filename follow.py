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
from .models import Friendship
# ------------------------------------------------------------------------------

follow = Blueprint('follow', __name__)


@follow.route('/follow')
@login_required
def friendship():
    results = []
    results.extend(Friendship.query.filter_by(
        followee=current_user.id).filter((Friendship.fstatus == 'accepted') | (Friendship.fstatus == 'pending')).all())
    results.extend(Friendship.query.filter_by(
        follower=current_user.id, fstatus='accepted').all())
    # print('-------------')
    # print(results)
    friend_id_list = []
    for r in results:
        friend_id_list.append(r.follower)
        friend_id_list.append(r.followee)

    friend_id_list_sorted = list(set(friend_id_list))
    friend_id_list_sorted.remove(current_user.id)

    users_friendship = []
    pending_count = 0
    for f in friend_id_list_sorted:
        friendship = Friendship.query.filter_by(
            follower=current_user.id, followee=f, fstatus='accepted').first()
        if not friendship:
            friendship = Friendship.query.filter_by(
                followee=current_user.id, follower=f, fstatus='accepted').first()
            if not friendship:
                friendship = Friendship.query.filter_by(
                    followee=current_user.id, follower=f, fstatus='pending').first()
                pending_count = pending_count + 1
        users_friendship.append(
            [Users.query.filter_by(id=f).first(), friendship])
    # print('-------------')
    # print(users_friendship)
    return render_template('following.html', users_friendship=users_friendship, pending_count=pending_count)


@follow.route('/follow', methods=['POST'])
@login_required
def friendship_post():
    follower = request.form.get('follower')
    followee = request.form.get('followee')
    action = request.form.get('action')
    print('-------------')
    print(action)
    if action == 'Unfollow':
        db.session.delete(Friendship.query.filter_by(
            follower=follower, followee=followee).first())
        db.session.commit()
    if action == 'Accept':
        Friendship.query.filter_by(follower=follower, followee=current_user.id, fstatus='pending').first().fstatus = 'accepted'
        db.session.commit()
    elif action == 'Reject':
        Friendship.query.filter_by(follower=follower, followee=current_user.id, fstatus='pending').first().fstatus = 'rejected'
        db.session.commit()

    return redirect(url_for('follow.friendship'))
