# -*- coding: utf-8 -*-

from gluon.tools import prettydate


db.define_table(
    'message',

    Field('context', length=25),
    Field('context_id', 'integer'),
    Field(
        'auth_user', 'reference auth_user', label=T('User'),
        requires=
            IS_EMPTY_OR(
                IS_IN_DB(
                    db, 'auth_user.id', db.auth_user._format,
                    # orderby=db.auth_user.title
                )
            )
    ),
    Field(
        'direction', length=8, label=T('Direction'),
        requires=IS_IN_SET(['Sent', 'Received'])
    ),
    Field('is_read', 'boolean', label=T('Read?')),
    Field('msg_sender', length=100, label=T('Sender')),
    Field('msg_from', length=100, label=T('From')),
    Field('msg_recipient', length=100, label=T('Recipient')),
    Field('msg_to', length=100, label=T('To')),
    Field('msg_subject', length=100, label=T('Subject')),
    Field('msg_body', length=500, label=T('Body')),
    Field('msg_html', length=500, label=T('Body HTML')),
    # Field('msg_attachments', 'file'),

    auth.signature,
    singular = 'Message', plural = 'Messages',
    format = '%(msg_from)s: %(msg_subject)s',
)

db.message.is_read.represent = lambda is_read, row: (
    XML(DIV(I(_class="fa fa-envelope-o"), ' Read')) if is_read
    else XML(DIV(I(_class="fa fa-envelope"), ' Unread'))
)
db.message.created_on.represent = lambda create_on, row: prettydate(create_on, T)
db.message.modified_on.represent = lambda modified_on, row: prettydate(modified_on, T)
