# coding: utf8

auth.settings.auth_manager_role = 'Admin' # for access to /appadmin/manage/auth

'''
course_fields = [db.course.title, db.course.credit, db.course.duration, db.course.grade]
db.course.id.readable = False
db.course.applicant.readable = db.course.applicant.writable = False
'''

auth.settings.manager_actions = dict(

    # appadmin/manage/users
    users=dict(
        role='Admin',
        tables=[db.auth_user, db.auth_membership],
        smartgrid_args=dict(
            DEFAULT=dict(
                maxtextlength=50, paginate=10,
                csv=True, searchable=True
            ),
            auth_user=dict(linked_tables=[]),
            # test=dict(fields=test_fields),
            # activity=dict(fields=activity_fields),
            # essay=dict(fields=essay_fields)
        )
    ),

    # appadmin/manage/statuses
    # statuses=dict(
    #     role='Admin',
    #     tables=[db.person, db.dog],
    #     smartgrid_args=dict(
    #         DEFAULT=dict(
    #             maxtextlength=50, paginate=10,
    #             csv=False, searchable=False
    #         ),
    #     )
    # ),

    # appadmin/manage/db
    db=dict(
        role='Admin',
        heading='Manage Database',
        tables=db.tables,
        smartgrid_args=dict(
            DEFAULT=dict(
                linked_tables=[],
                maxtextlength=50, paginate=10,
                csv=True, searchable=True
            ),
        )
    ),

)
