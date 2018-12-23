db.define_table(
    'notification',
    Field(
        'title',
        'string',
        length=140,
    ),
    Field(
        'type',
        'string',
        length=15,
        requires=IS_EMPTY_OR(
            IS_IN_SET(
                [
                    'user', 'cake',
                ]
            )
        )
    ),
    Field('is_read', 'boolean', label=T('Read?')),
    Field(
        'auth_user',
        'reference auth_user',
    ),
    auth.signature,
    singular='Notification', plural='Notifications',
    format='%(title)s',
    )
