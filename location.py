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
from .models import Blocks
from .models import Hood
from .models import Location
from .models import Membership
from .models import Approval
# ------------------------------------------------------------------------------

location = Blueprint('location', __name__)


@location.route('/blocks')
@login_required
def blocks():
    my_membership = get_my_membership()
    if my_membership:
        my_block_id = my_membership.bid
        if my_membership.approval_count == -1:
            status = 'Joined'
        else:
            status = 'Pending'
        # Find all [blocks_id, hood_id] ids (exclude the one you're in) in your city
        blocks_hood_id_list = []
        for i in Location.query.filter_by(cid=current_user.cid).all():
            if i.bid != my_block_id:
                blocks_hood_id_list.append([i.bid, i.hid])
            else:
                my_hood_id = i.hid
        # Find all [blocks, hood] ids (exclude the one you're in) in your city
        blocks_hood_list = []
        for i in blocks_hood_id_list:
            blocks_hood_list.append([Blocks.query.filter_by(
                id=i[0]).first(), Hood.query.filter_by(id=i[1]).first()])
        # Your own [block, hood]
        my_blocks_hood_id = [my_block_id, my_hood_id]
        my_blocks_hood = [Blocks.query.filter_by(id=my_blocks_hood_id[0]).first(
        ), Hood.query.filter_by(id=my_blocks_hood_id[1]).first()]

        return render_template('blocks.html', status=status, my_blocks_hood=my_blocks_hood, blocks_hood=blocks_hood_list)
    else:
        # Find all [blocks_id, hood_id] ids in your city
        blocks_hood_id_list = []
        for i in Location.query.filter_by(cid=current_user.cid).all():
            blocks_hood_id_list.append([i.bid, i.hid])
        blocks_hood_list = []
        # Find all [blocks, hood] ids in your city
        for i in blocks_hood_id_list:
            blocks_hood_list.append([Blocks.query.filter_by(
                id=i[0]).first(), Hood.query.filter_by(id=i[1]).first()])
        return render_template('blocks.html', blocks_hood=blocks_hood_list)


@location.route('/blocks', methods=['POST'])
@login_required
def join_block():
    to_join_block_id = request.form.get('to-join')
    if get_my_membership():
        db.session.delete(get_my_membership())
        db.session.commit()
    db.session.add(Membership(uid=current_user.id,
                              bid=to_join_block_id, approval_count=0))
    db.session.commit()
    flash('You are joining %s. Membership is pending approval' %
          Blocks.query.filter_by(id=to_join_block_id).first().bname)

    return redirect(url_for('location.blocks'))


@login_required
def get_my_membership():
    return Membership.query.filter_by(uid=current_user.id).first()


@location.route('/block-members')
@login_required
def block_members():
    my_membership = get_my_membership()
    if my_membership:
        if my_membership.approval_count == -1:

            my_block_id = get_my_membership().bid

            # Get pending members to approve:
            pending = Membership.query.filter(
                Membership.bid == my_block_id, Membership.approval_count > -1).all()
            pending_count = len(pending)
            print('-------------------')
            print(pending)
            print(pending_count)
            # Remove those already approved by you
            approved_by_you = Approval.query.filter_by(
                approver=current_user.id, bid=my_block_id).all()
            approved_by_you_uid_list = []
            if approved_by_you:
                for i in approved_by_you:
                    approved_by_you_uid_list.append(i.approvee)
            # Convert them to [Users, Membership] pair
            pending_users_membership = []
            for i in pending:
                if i.uid not in approved_by_you_uid_list:
                    pending_users_membership.append(
                        [Users.query.filter_by(id=i.uid).first(), i])

            # Get approved members
            approved = Membership.query.filter(
                Membership.bid == my_block_id, Membership.approval_count < 0).all()
            approved_count = len(approved)
            print('-------------------')
            print(approved)
            print(pending_count)

            # Convert them to [Users, Membership] pair
            approved_users_membership = []
            for i in approved:
                approved_users_membership.append(
                    [Users.query.filter_by(id=i.uid).first(), i])

        elif my_membership.approval_count > -1:
            return render_template('block-members.html', status='Pending')
        else:
            return render_template('block-members.html', status='Not')

    return render_template('block-members.html', pending_count=pending_count, pending_users_membership=pending_users_membership, approved_users_membership=approved_users_membership, approved_count=approved_count)


@location.route('/block-members', methods=['POST'])
@login_required
def block_members_post():
    if request.form.get('action') == 'Approve' and request.form.get('uid') and request.form.get('bid'):
        membership = Membership.query.filter_by(
            uid=request.form.get('uid'), bid=request.form.get('bid')).first()
        if membership.approval_count != -1:
            # Approve or not based on block population
            membership.approval_count += 1
            db.session.add(Approval(approver=current_user.id, approvee=request.form.get(
                'uid'), bid=request.form.get('bid')))
            db.session.commit()
            flash('You have approved this user to join your block')
            if membership.approval_count >= 3 or membership.approval_count == Blocks.query.filter_by(id=request.form.get('bid')).first().bpopulation:
                membership.approval_count = -1
                db.session.commit()

    return redirect(url_for('location.block_members'))


@location.route('/map')
@login_required
def map():
    return render_template('map.html')