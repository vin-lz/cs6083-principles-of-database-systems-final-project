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
from .models import Location
# ------------------------------------------------------------------------------


timeline = Blueprint('timeline', __name__)


@timeline.route('/timeline')
@login_required
def load_thread(scope='all', status='all', search=False, keyword=""):
    # Handle the search
    if search:
        to_search = '%{}%'.format(keyword)
        print("---------to search-----")
        print(to_search)
        message_list = Message.query.filter(Message.content.like(to_search) | Message.title.like(to_search)).all()
        print("----message_list-----")
        print(message_list)
        thread_list = []
        for i in message_list:
            to_display = Thread.query.filter_by(uid=current_user.id, mid=i.id).first()
            if to_display != None:
                thread_list.append(to_display)
        in_scope_thread_message_users_list = []
        count = 0
        print('---- all thread_list----')
        print(thread_list)
        for i in thread_list:
            message = Message.query.filter_by(id=i.mid).first()
            author = Users.query.filter_by(id=message.author).first()
            in_scope_thread_message_users_list.append([i, message, author])
            count += 1
        
        return render_template('timeline.html', message_count=count, thread_message_list=in_scope_thread_message_users_list, search=search)


    # Gather all thread
    print('---- parameters----')
    print(scope, status)
    thread_list = Thread.query.filter_by(uid=current_user.id).all()
    count = 0
    in_scope_thread_message_users_list = []
    print('---- all thread_list----')
    print(thread_list)

    for i in thread_list:
        if scope == 'own':
            message = Message.query.filter_by(id=i.mid).first()
            if message.author == current_user.id:
                author = Users.query.filter_by(id=message.author).first()
                in_scope_thread_message_users_list.append([i, message, author])
                count += 1
        elif scope != 'all':
            message = Message.query.filter_by(id=i.mid).first()
            if message.visibility == scope:
                author = Users.query.filter_by(id=message.author).first()
                if author.id != current_user.id:
                    in_scope_thread_message_users_list.append([i, message, author])
                    count += 1
        else:
            if status == 'unread':
                if i.tstatus == 'unread':
                    message = Message.query.filter_by(id=i.mid).first()
                    author = Users.query.filter_by(id=message.author).first()
                    if author.id != current_user.id:
                        in_scope_thread_message_users_list.append([i, message, author])
                        count += 1
            elif status == 'new':
                if i.ttimestamp > current_user.last_logout_timestamp:
                    message = Message.query.filter_by(id=i.mid).first()
                    author = Users.query.filter_by(id=message.author).first()
                    if author.id != current_user.id:
                        in_scope_thread_message_users_list.append([i, message, author])
                        count += 1
            else:
                message = Message.query.filter_by(id=i.mid).first()
                author = Users.query.filter_by(id=message.author).first()
                if author.id != current_user.id:
                    in_scope_thread_message_users_list.append([i, message, author])
                    count += 1

    print("count %d" % count)
    return render_template('timeline.html', message_count=count, thread_message_list=in_scope_thread_message_users_list, scope=scope, status=status)


@timeline.route('/timeline', methods=['POST'])
@login_required
def load_thread_filtered():
    if request.form.get('search') == 'True':
        return load_thread(search=True, keyword=request.form.get('keyword'))
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
    new_message = Message(author=current_user.id, title=title, content=content, mtimestamp=datetime.now().replace(microsecond=0), visibility=visibility)
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

    posted = Message.query.filter_by(author=current_user.id, mtimestamp=new_message.mtimestamp).first()

    print('---posted---')
    print(posted)

    # Add thread entry for every users in that hood
    if posted.visibility == 'hood':
        membership = Membership.query.filter_by(uid=current_user.id).first()
        if membership:
            bid = membership.bid
            hid = Location.query.filter_by(bid=bid).first().hid
            blocks_in_hood = Location.query.filter_by(hid=hid).all()
            bid_list = []
            for i in blocks_in_hood:
                bid_list.append(i.bid)
            members_in_hood = []
            for i in bid_list:
                members_in_hood.extend(Membership.query.filter_by(bid=i).all())
            users_list = []
            for i in members_in_hood:
                users_list.append(Users.query.filter_by(id=i.uid).first())
        for i in users_list:
            new_thread = Thread(uid=i.id, mid=posted.id, tstatus='unread', ttimestamp=posted.mtimestamp)
            db.session.add(new_thread)
            db.session.commit()
    
    # Add thread entry for every users in that block
    if posted.visibility == 'block':
        membership = Membership.query.filter_by(uid=current_user.id).first()
        if membership:
            bid = membership.bid
            members_in_block = Membership.query.filter_by(bid=bid).all()
            users_list = []
            for i in members_in_block:
                users_list.append(Users.query.filter_by(id=i.uid).first())
        for i in users_list:
            new_thread = Thread(uid=i.id, mid=posted.id, tstatus='unread', ttimestamp=posted.mtimestamp)
            db.session.add(new_thread)
            db.session.commit()

    # Add thread entry for every friend
    if posted.visibility == 'friend':
        results = []
        results.extend(Friendship.query.filter_by(
        followee=current_user.id, fstatus='accepted').all())
        results.extend(Friendship.query.filter_by(
        follower=current_user.id, fstatus='accepted').all())
        friend_id_list = []
        for i in results:
            friend_id_list.append(i.follower)
            friend_id_list.append(i.followee)
        friend_id_list_sorted = list(set(friend_id_list))
        for i in friend_id_list_sorted:
            new_thread = Thread(uid=i, mid=posted.id, tstatus='unread', ttimestamp=posted.mtimestamp)
            db.session.add(new_thread)
            db.session.commit()

    # Add thread entry for directed message target user
    if posted.visibility == 'direct':
        target = Users.query.filter_by(email=directed).first()
        new_thread = Thread(uid=target.id, mid=posted.id, tstatus='unread', ttimestamp=posted.mtimestamp)
        db.session.add(new_thread)
        db.session.commit()

    flash('Message posted successfully')
    return redirect(url_for('timeline.load_thread')) 


@timeline.route('/post/<int:post_id>/', methods=['POST'])
@login_required
def new_reply_post(post_id):
    if not request.form.get('content'):
        flash('Reply cannot be empty')
        return redirect(url_for('timeline.display_message', post_id=post_id))
    else:
        content = request.form.get('content')
        new_reply = Reply(mid=post_id, author=current_user.id, content=content, rtimestamp=datetime.now().replace(microsecond=0))
        db.session.add(new_reply)
        db.session.commit()

        thread_list = Thread.query.filter_by(mid=post_id).all()
        for i in thread_list:
            i.tstatus = 'unread'
            i.ttimestamp = datetime.now().replace(microsecond=0)
        db.session.commit()
        flash('Reply successful')
        return redirect(url_for('timeline.display_message', post_id=post_id))

