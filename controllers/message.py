# -*- coding: utf-8 -*-

import requests

table = db.message
response.view_title = '%s %s' % (
    table._singular,
    request.function.replace('_', ' ').title()
)


def index():
    redirect(URL(request.controller, 'list'))


def list():
    announcement = None  # XML(response.render('announcement.html'))
    query = (table)
    items = db(query).select(orderby=~table.created_on).render()

    # fields = [f for f in table]
    fields = [
        table.context, table.context_id,
        table.direction, table.is_read,
        table.auth_user,
        table.created_on,
        table.msg_subject
    ]

    return dict(
        item_name=table._singular,
        row_list=items,
        field_list=fields,
        announcement=announcement
    )


@auth.requires_login()
def create():
    table.direction.default = 'Sent'
    table.is_read.default = True

    # auth_user is optional to allow receipt of messages from unknown senders
    # so we need to require it now
    table.auth_user.requires = IS_IN_DB(db, 'auth_user.id', db.auth_user._format)

    fields = [
        'auth_user',
        'msg_subject',
        'msg_body',
    ]

    form = SQLFORM(table, fields=fields)

    if form.process().accepted:

        user = db(db.auth_user.id == request.vars.auth_user).select().first()

        send_mailgun_message(
            user.email,
            form.vars.msg_subject,
            form.vars.msg_body
        )

        session.flash = '%s sent!' % table._singular
        redirect(URL(request.controller, 'list'))

    elif form.errors:

        response.flash = 'Please correct the errors'

    response.view = 'template/create.html'
    return dict(item_name=table._singular, form=form)


def reply():
    item = table(table.id == request.args(0)) or redirect(URL('index'))

    # update read flag
    if not item.is_read:
        item.is_read = True
        item.update_record()

    table.auth_user.default = item.auth_user
    table.auth_user.writable = False
    table.direction.default = 'Sent'
    table.is_read.default = True
    table.msg_to.default = item.msg_from
    table.msg_subject.default = "Re: %s" % item.msg_subject

    fields = [
        'auth_user',
        'msg_subject',
        'msg_body',
    ]

    form = SQLFORM(table, fields=fields)

    if form.process().accepted:

        send_mailgun_message(
            item.msg_from,
            form.vars.msg_subject,
            form.vars.msg_body
        )

        session.flash = '%s created!' % table._singular
        redirect(URL(request.controller, 'list'))

    elif form.errors:

        response.flash = 'Please correct the errors'

    return dict(item_name=table._singular, form=form, item=item)


def view():
    item = table(table.id == request.args(0)) or redirect(URL('index'))

    # update read flag
    if not item.is_read:
        item.is_read = True
        item.update_record()

    fields = [
        'direction',
        'auth_user',
        'created_on',
        'msg_subject',
        'msg_body',
    ]

    table.created_on.readable = True

    form = SQLFORM(table, item, fields=fields, readonly=True, comments=False)

    return dict(item_name=table._singular, form=form, item=item)


def send_mailgun_message(msg_to, msg_subject, msg_body):

    sender_name = myconf.get('mailgun.sender_name')
    sender_id = myconf.get('mailgun.sender_id')
    sender_domain = myconf.get('mailgun.sender_domain')
    private_api_key = myconf.get('mailgun.private_api_key')

    requests.post(
        "https://api.mailgun.net/v3/%s/messages" % sender_domain,
        auth=("api", "%s" % private_api_key),
        data={
            "from": "%s <%s@%s>" % (sender_name, sender_id, sender_domain),
            "to": msg_to,
            "subject": msg_subject,
            "text": msg_body
        }
    )

    return


def receive_mailgun_message():
    # https://documentation.mailgun.com/user_manual.html#routes

    query = db.auth_user.email == request.vars['sender']
    user = db(query).select().first()

    db.message.insert(
        direction = 'Received',
        auth_user = user.id if user else None,
        msg_sender = request.vars['sender'],
        msg_from = request.vars['From'],
        msg_recipient = request.vars['recipient'],
        msg_to = request.vars.To,
        msg_subject = request.vars.subject,
        msg_body = request.vars['stripped-text'],
        msg_html = request.vars['stripped-html'],
    )

    return


def menu():
    query = ((table.is_read == None) | (table.is_read == False))
    items = db(query).select(orderby=~table.created_on)

    return dict(unread_messages=items)
