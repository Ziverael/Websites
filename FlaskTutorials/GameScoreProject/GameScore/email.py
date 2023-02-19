"""
TO DO
------------
despite running different threads just prepare dedicated job for sending emails, e.g. Celery tasj queue
"""

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message
from . import mail

def send_async_email(app, msg):
    """Send email without blocking the main web thread"""
    with app.context():
        mail.send(msg)
    

def send_email(to, subject, template, **kwargs):
    """
    Send email.
    
    It's worth to notice that because of using different thread, the application context is artificially reproduced.
    """
    
    app = current_app._get_current_object()
    msg = Message(
        app.config['APP_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
        sender = app.config['APP_MAIL_SENDER'],
        recipients = [to]
        )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target = send_async_email, args = [app, msg])
    thr.start()
    return thr