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
from .models import Neighboring
# ------------------------------------------------------------------------------

follow = Blueprint('follow', __name__)


@follow.route('/friends')
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
    if current_user.id in friend_id_list_sorted:
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
    return render_template('friends.html', users_friendship=users_friendship, pending_count=pending_count, accepted_count=len(users_friendship)-pending_count)


@follow.route('/friends', methods=['POST'])
@login_required
def friendship_post():
    # Add new friend
    if request.form.get('add-new'):
        if not request.form.get('friend-email'):
            flash('Your need an email to follow a user.')
        else:
            to_add = request.form.get('friend-email')
            print(to_add, 'friend')
            new_follow(to_add, 'friend')
            return redirect(url_for('follow.friendship'))

    follower = request.form.get('follower')
    followee = request.form.get('followee')
    action = request.form.get('action')
    # print('-------------')
    # print(action)
    if action == 'Unfollow':
        db.session.delete(Friendship.query.filter_by(
            follower=follower, followee=followee).first())
        db.session.commit()
        if follower == current_user.id:
            flash('You has unfollowed %s %s' % (Users.query.filter_by(
                id=followee).first().fname, Users.query.filter_by(id=followee).first().lname))
        else:
            flash('You has unfollowed %s %s' % (Users.query.filter_by(
                id=follower).first().fname, Users.query.filter_by(id=follower).first().lname))
    if action == 'Accept':
        Friendship.query.filter_by(
            follower=follower, followee=current_user.id, fstatus='pending').first().fstatus = 'accepted'
        db.session.commit()
        flash('You has accepted %s %s\'s friend request' % (Users.query.filter_by(
            id=follower).first().fname, Users.query.filter_by(id=follower).first().lname))
    elif action == 'Reject':
        Friendship.query.filter_by(
            follower=follower, followee=current_user.id, fstatus='pending').first().fstatus = 'rejected'
        db.session.commit()
        flash('You has rejected %s %s\'s friend request' % (Users.query.filter_by(
            id=follower).first().fname, Users.query.filter_by(id=follower).first().lname))

    return redirect(url_for('follow.friendship'))


@follow.route('/neighbors')
@login_required
def neighbor():
    results = []
    results.extend(Neighboring.query.filter_by(
        initiator=current_user.id).all())

    neighbor_id_list = []
    for r in results:
        neighbor_id_list.append(r.acceptor)

    neighbor_id_list_sorted = sorted(neighbor_id_list)

    users_neighboring = []
    neighbor_count = 0
    for n in neighbor_id_list_sorted:
        users_neighboring.append([Users.query.filter_by(id=n).first(
        ), Neighboring.query.filter_by(initiator=current_user.id, acceptor=n).first()])
        neighbor_count = neighbor_count + 1

    return render_template('neighbors.html', users_neighboring=users_neighboring, neighbor_count=neighbor_count)


@follow.route('/neighbors', methods=['POST'])
@login_required
def neighbor_post():
    # Add new neighbor
    if request.form.get('add-new'):
        if not request.form.get('neighbor-email'):
            flash('Your need an email to follow a user.')
        else:
            to_add = request.form.get('neighbor-email')
            print(to_add, 'neighbor')
            new_follow(to_add, 'neighbor')
            return redirect(url_for('follow.neighbor'))

    acceptor = request.form.get('neighbor')
    action = request.form.get('action')
    if action == 'Unfollow':
        db.session.delete(Neighboring.query.filter_by(
            initiator=current_user.id, acceptor=acceptor).first())
        db.session.commit()
        flash('You has unfollowed %s %s' % (Users.query.filter_by(
            id=acceptor).first().fname, Users.query.filter_by(id=acceptor).first().lname))

    return redirect(url_for('follow.neighbor'))

@login_required
def new_follow(email, category):
    print(email, category)
    if category == 'friend':
        followee = Users.query.filter_by(email=email).first()
        print(followee)
        if followee:
            if not Friendship.query.filter_by(follower=current_user.id, followee=followee.id).first() and not Friendship.query.filter_by(follower=followee.id, followee=current_user.id).first():
                
                new_friendship = Friendship(follower=current_user.id, followee=followee.id, ftimestamp=datetime.now(), fstatus='pending')
                db.session.add(new_friendship)
                db.session.commit()
                flash('An invitation has been sent.')
            else:
                flash('Already in your friend list.')
        else:
            flash('Can\'t find this user in the system.')
    elif category == 'neighbor':
        followee = Users.query.filter_by(email=email).first()
        print(followee)
        if followee:
            if not Neighboring.query.filter_by(initiator=current_user.id, acceptor=followee.id).first():
                
                new_neighbor = Neighboring(initiator=current_user.id, acceptor=followee.id, ntimestamp=datetime.now())
                db.session.add(new_neighbor)
                db.session.commit()
                flash('A neighbor is added.')
            else:
                flash('Already in your neighbor list.')
        else:
            flash('Can\'t find this user in the system.')

    return