db.define_table(
    'notification',
    Field(
        'title',
        'string',
        length=140,
    ),
    Field(
        'user',
        'reference auth_user',
    ),
    auth.signature,
    singular='Notification', plural='Notifications',
    format='%(title)s',
)