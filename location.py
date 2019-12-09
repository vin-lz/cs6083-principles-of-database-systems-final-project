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
# ------------------------------------------------------------------------------

location = Blueprint('location', __name__)

@location.route('/blocks')
@login_required
def blocks():
    my_membership = get_my_membership()
    if my_membership:
        my_block_id = my_membership.bid
    else:
        my_block_id = None

    blocks_hood_id_list = []
    for l in Location.query.filter_by(cid=current_user.cid).all():
        if l.bid != my_block_id:
            blocks_hood_id_list.append([l.bid, l.hid])
        else:
            my_hood_id = l.hid

    blocks_hood_list = []
    for i in blocks_hood_id_list:
        blocks_hood_list.append([Blocks.query.filter_by(id=i[0]).first(), Hood.query.filter_by(id=i[1]).first()])

    if my_block_id:
        my_blocks_hood_id = [my_block_id, my_hood_id]
        my_blocks_hood = [Blocks.query.filter_by(id=my_blocks_hood_id[0]).first(), Hood.query.filter_by(id=my_blocks_hood_id[1]).first()]

        return render_template('blocks.html', my_blocks_hood=my_blocks_hood, blocks_hood=blocks_hood_list)

    print(blocks_hood_list)
    return render_template('blocks.html', blocks_hood=blocks_hood_list)


@location.route('/blocks', methods=['POST'])
@login_required
def join_block():
#     location = Location.query.filter_by(bid=block.id, cid=current_user.cid)
#     hood = Hood.query.filter_by(id=Location.query.filter_by(block.))
    return redirect(url_for('location.blocks'))

def get_my_membership():
    return Membership.query.filter_by(uid=current_user.id).first()
