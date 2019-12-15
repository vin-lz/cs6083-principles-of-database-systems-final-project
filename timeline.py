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