# -*- coding: utf-8 -*-

STATUSES = [
    ['1', 'Happy'],
    ['2', 'Sad'],
]

db.define_table(
    'person',

    Field('title', length=25, requires=[IS_NOT_EMPTY(), Titleize()]),
    Field('auth_user', 'reference auth_user'),

    Field('addr_street', length=50, label='Street'),
    Field('addr_city', length=50, label='City'),
    Field('addr_state', length=50, label='State/Province'),
    Field('addr_zip', length=50, label='ZIP/Postal code'),

    Field('phone', length=50, label='Phone'),
    Field('fax', length=50, label='Fax'),

    Field('string_list', length=25,
          requires=IS_IN_SET(['Regional', 'Corporate', 'Local', 'Other'], zero=None)),
    Field('status', 'integer', label='Status',
          requires=IS_IN_SET(STATUSES, zero=None)),

    auth.signature,
    singular='Dog Lover', plural='Dog Lovers',
    format='%(title)s',
)

db.define_table(
    'dog',

    Field('title', length=100, requires=[IS_NOT_EMPTY(), Titleize()]),

    auth.signature,
    singular='Dog', plural='Dogs',
    format='%(title)s',
)

db.define_table(
    'dog_owner',

    Field('person', 'reference person'),
    Field(
        'dog', 'reference dog',
        # requires=
        #     IS_IN_DB(
        #         db, 'dog.id', db.dog._format,
        #         orderby=db.dog.title
        #     )
    ),

    auth.signature,
    singular='Dog Owner', plural='Dog Owners',
    format="%(person)s's %(dog)s",
)
