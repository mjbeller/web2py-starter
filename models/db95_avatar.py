db.define_table(
    'avatar',
    Field(
        'image',
        'string',
        length = 100,
        requires = IS_IN_SET(
            [
                'img/avatar.png',
                'img/avatar2.png',
                'img/avatar3.png',
                'img/avatar4.png',
                'img/avatar5.png',
            ]
        )
    ),
    Field(
        'auth_user',
        'reference auth_user',
        label=T('User'),
    ),
    auth.signature,
    singular = 'Avatar', plural = 'Avatars',
    format = '%(avatar)s',
)
