db.define_table(
    'task',
    Field(
        'title',
        'string',
        length=140,
    ),
    Field(
        'criteria',
        'list:string',
        requires=IS_IN_SET([
            0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100
        ]),
    ),
    Field(
        'user',
        'reference auth_user',
    ),
    auth.signature,
    singular='Task', plural='Tasks',
    format='%(title)s',
)