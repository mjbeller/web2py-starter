# -*- coding: utf-8 -*-

if not request.is_local:
    redirect(URL('default', 'index'))


def adminuser():
    # http://stackoverflow.com/questions/10201300/how-can-i-create-new-auth-user-and-auth-group-on-web2py-running-on-google-app-en
    if not db().select(db.auth_user.ALL).first():
        db.auth_user.insert(
            username=myconf.get('admin_user.username'),
            password=db.auth_user.password.validate(myconf.get('admin_user.password'))[0],
            email=myconf.get('admin_user.email'),
            first_name=myconf.get('admin_user.first_name'),
            last_name=myconf.get('admin_user.last_name'),
        )

        user = auth.login_bare(
            myconf.get('admin_user.username'),
            myconf.get('admin_user.password')
        )

        authgroups()
        fixauthgroups()
        # appstatuses()
        populate(db.person)
        populate(db.dog)
        populate(db.dog_owner)

    redirect(URL('default', 'index'))


def authgroups():
    if not db().select(db.auth_group.ALL).first():
        for group in myconf.get('admin_user.auth_groups'):
            db.auth_group.insert(
                role=group
            )
        db.auth_membership.insert(
            user_id=1,
            group_id=1
        )
    return


def fixauthgroups():
    GROUPS = db().select(db.auth_group.ALL)
    for group in GROUPS:
        group.update_record(
            role=group.role.title()
        )
    return


def appstatuses():
    db.application_status.truncate()
    db.application_status.bulk_insert([
        {'title': 'New'},
        {'title': 'Pre Approved'},
        {'title': 'Approved'},
        {'title': 'Denied'},
        {'title': 'Active'},
        {'title': 'Closed'},
    ])
    return


def populate(table):
    query = table
    set = db(query)
    # rows = set.select()
    set.delete()
    from gluon.contrib.populate import populate
    populate(table, 15)
    return
