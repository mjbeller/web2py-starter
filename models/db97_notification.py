db.define_table(
    'notification',
    Field(
        'title',
        'string',
        length=140,
    ),
    Field(
        'auth_user',
        'reference auth_user',
    ),
    auth.signature,
    singular='Notification', plural='Notifications',
    format='%(title)s',
)