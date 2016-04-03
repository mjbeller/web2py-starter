# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.view_title = 'web2py Starter App'
    return dict(message='')


def about():
    response.view_title = 'About'
    return dict()


def tou():
    response.view_title = 'Terms of Use'
    return dict()


def privacy():
    response.view_title = 'Privacy Policy'
    return dict()


def changelog():
    response.view_title = 'Changelog and 3rd Party Services'

    import os
    changelog_markmin = MARKMIN('')
    infile = open(os.path.join(request.folder, 'CHANGELOG'))
    for line in infile:
        changelog_markmin += MARKMIN(line)

    return dict(changelog_markmin=changelog_markmin)


def search():
    tables = [db.dog, db.person]

    items = []
    for t in tables:
        fields = [
            t.id, t.title,
            t.created_on, t.created_by,
        ]
        query = (t.title.contains(request.vars['q']))
        rows = db(query).select(*fields).render()
        for r in rows:
            items += [[t._singular, r.id, r.title, r.created_on, r.created_by]]

    response.view_title = 'Search Results'
    return dict(
        items=items
    )


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    response.view_title = ''

    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
