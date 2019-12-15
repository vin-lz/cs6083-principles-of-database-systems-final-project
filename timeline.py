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
from .models import Blocks
from .models import Membership
from .models import Thread
from .models import Message
from .models import Reply
# ------------------------------------------------------------------------------


timeline = Blueprint('timeline', __name__)


@timeline.route('/timeline')
@login_required
def load_thread(scope='all', status='all'):
    # status = 'unread'
    # scope='hood'
    # Gather all thread
    print('---- parameters----')
    print(scope, status)
    thread_list = Thread.query.filter_by(uid=current_user.id).all()
    count = 0
    in_scope_thread_message_list = []
    print('---- all thread_list----')
    print(thread_list)
    # When display all
    if scope == 'all':
        if status == 'unread':
            for i in thread_list:
                if i.tstatus != 'unread':
                    thread_list.remove(i)
        for i in thread_list:
            message = Message.query.filter_by(id=i.mid).first()
            author = Users.query.filter_by(id=message.author).first()
            in_scope_thread_message_list.append([i, message, author])
            count += 1
        return render_template('timeline.html', message_count=count, thread_message_list=in_scope_thread_message_list)

    # Filter to find those meeting the scope
    for i in thread_list:
        message = Message.query.filter_by(id=i.mid).first()
        if message.visibility == scope:
            author = Users.query.filter_by(id=message.author).first()
            in_scope_thread_message_list.append([i, message, author])
            count += 1
    print('----in_scope_thread_message_list----')
    print(in_scope_thread_message_list)

    # If unread only
    if status == 'unread':
        for i in in_scope_thread_message_list:
            if i[0].tstatus != 'unread':
                in_scope_thread_message_list.remove(i)
                count -= 1
    print('----unread_in_scope_thread_message_list----')
    print(in_scope_thread_message_list)

    return render_template('timeline.html', message_count=count, thread_message_list=in_scope_thread_message_list)


@timeline.route('/timeline', methods=['POST'])
@login_required
def load_thread_filtered():
    scope = request.form.get('scope')
    status = request.form.get('status')
    return load_thread(scope, status)


@timeline.route('/post/<int:post_id>/', methods=['GET'])
@login_required
def display_message(post_id):
    if not Thread.query.filter_by(uid=current_user.id, mid=post_id).first():
        flash('You have no privilege to read this post')
        return redirect(url_for('timeline.load_thread'))

    message_info = {
        'message': Message.query.filter_by(id=post_id).first(),
        'author': Users.query.filter_by(id=Message.query.filter_by(id=post_id).first().author).first(),
        'block': Blocks.query.filter_by(id=(Membership.query.filter_by(uid=Users.query.filter_by(id=Message.query.filter_by(id=post_id).first().author).first().id).first().bid)).first()
    }
    print('---------message---------')
    print(message_info)

    reply_list = Reply.query.filter_by(mid=post_id).all()
    reply_info_list = []
    if reply_list:
        for i in reply_list:
            reply_info = {
                'reply': i,
                'author': Users.query.filter_by(id=i.author).first(),
                'block': Blocks.query.filter_by(id=(Membership.query.filter_by(uid=i.author).first().bid)).first()
            }
            reply_info_list.append(reply_info)

    print('---------reply---------')
    print(reply_list)

    Thread.query.filter_by(uid=current_user.id,
                           mid=post_id).first().tstatus = 'read'
    db.session.commit()

    return render_template('post.html', message_info=message_info, reply_info_list=reply_info_list)

@timeline.route('/new-post')
@login_required
def new_post():
    return render_template('new-post.html')


@timeline.route('/new-post', methods=['POST'])
@login_required
def new_post_post():
    title = request.form.get('title')
    content = request.form.get('content')
    visibility = request.form.get('visibility')
    new_message = Message(author=current_user.id, title=title, content=content, mtimestamp=datetime.now(), visibility=visibility)
    if request.form.get('latitude') and request.form.get('longitude'):
        latitude = request.form.get('latitude')
        new_message.lat = latitude
        longitude = request.form.get('longitude')
        new_message.lng= longitude
    if visibility == 'direct':
        directed = request.form.get('direct-email')
        if Users.query.filter_by(email=directed).first():
            new_message.receiver = directed
        else:
            flash("User not found")
            return redirect(url_for('timeline.new_post'))  

    db.session.add(new_message)
    db.session.commit()
    flash('Message posted successfully')
    return redirect(url_for('timeline.load_thread')) 