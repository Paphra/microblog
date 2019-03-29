from flask import (render_template, redirect, request, jsonify,
                   current_app, flash, url_for)
from flask_login import current_user, login_required
from datetime import time, datetime
from app import db
from app.messages import bp
from app.models import User, Message, Notification
from app.messages.forms import MessageForm, MessageReplyForm
from flask_babel import _


@bp.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender=current_user, recipient=user,
                      body=form.message.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('main.user', username=recipient))
    return render_template('messages/send_message.html', title=_('Send Message'),
                           form=form, recipient=recipient)


@bp.route('/messages')
@login_required
def messages():
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)

    messages_received = current_user.messages_received
    messages_sent = current_user.messages_sent

    pagination = current_app.config['MESSAGES_PER_PAGE']
    msg_pg = messages_received.union(messages_sent).order_by(
        Message.timestamp.desc()).paginate(
            page, pagination, False)

    pair = []
    recipients = []
    senders = []
    messages = []
    for message in msg_pg.items:
        sender = message.sender.username
        recipient = message.recipient.username

        users = [sender, recipient]
        if sender not in senders and users not in pair:
            messages.append(message)
            pair.append(pair)

    next_url = None
    prev_url = None

    if msg_pg.next_num and len(messages) > pagination:
        next_url = url_for('messages.messages', page=msg_pg.next_num)
    if msg_pg.prev_num and len(messages) > pagination:
        prev_url = url_for('messages.messages', page=msg_pg.prev_num)

    return render_template('messages/messages.html', messages=messages,
                           next_url=next_url, prev_url=prev_url,
                           title=_('Messages'))

@bp.route('/user_messages/<username>', methods=['GET', 'POST'])
@login_required
def user_messages(username):

    form = MessageReplyForm()
    user = User.query.filter_by(username=username).first_or_404()

    if form.validate_on_submit():
        msg = Message(sender=current_user, recipient=user,
                        body=form.reply.data)
        db.session.add(msg)
        user.add_notification('unread_message_count', user.new_messages())
        db.session.commit()
        return redirect(url_for('messages.user_messages', username=username))

    page = request.args.get('page', 1, type=int)

    messages_received = current_user.messages_received.filter_by(sender=user)
    messages_sent = current_user.messages_sent.filter_by(recipient=user)

    messages = messages_received.union(messages_sent).order_by(
        Message.timestamp.desc()).paginate(
            page, current_app.config['MESSAGES_PER_PAGE'], False)

    for m in messages.items:
        if m.recipient == current_user:
            m.set_status(1)
    db.session.commit()

    next_url = url_for('messages.user_messages', username=username,
                       page=messages.next_num) if messages.has_next else None
    prev_url = url_for('messages.user_messages', username=username,
                       page=messages.prev_num) if messages.has_prev else None

    return render_template('messages/user_messages.html', messages=messages.items,
                           next_url=next_url, prev_url=prev_url, user=user,
                           form=form, title=_('User Messages'))

@bp.route('/notifications')
@login_required
def notifications():
    since = request.args.get('since', 0.0, type=float)
    notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(
            Notification.timestamp.asc())

    return jsonify([{
        'name': n.name,
        'data': n.get_data(),
        'timestamp': n.timestamp
    } for n in notifications])
