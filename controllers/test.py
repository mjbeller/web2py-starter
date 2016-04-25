# -*- coding: utf-8 -*-

'''This is a controller to test different plugins and
then serve as a template for plugins, e.g., bootbox and selectize
'''

table = db.dog_owner
response.view_title = '%s %s' % (
    request.function.replace('_', ' ').title(),
    table._singular
)


def test_selectize():
    return dict()


def test_bootbox():
    return dict()


def index():
    redirect(URL(request.controller, 'list'))


def list():
    announcement = None  # XML(response.render('announcement.html'))
    query = (table)
    items = db(query).select(orderby=~table.created_on).render()

    actions = [
        {'is_item_action': lambda item: True, 'url': lambda item: URL('view.html', args=[item.id]), 'icon': 'search'},
        {'is_item_action': lambda item: True, 'url': lambda item: URL('edit.html', args=[item.id]), 'icon': 'pencil'},
    ]

    fields = [f for f in table]
    # fields = [
    #     table.id,
    #     table.created_on, table.created_by,
    # ]

    response.view = 'template/list.%s' % request.extension
    return dict(
        item_name=table._singular,
        row_list=items,
        actions=actions,
        field_list=fields,
        announcement=announcement
    )


@auth.requires_login()
def create():
    fields = [
        'id',
        'created_on', 'created_by',
    ]

    form = SQLFORM(table)  # , fields=fields)

    if form.process().accepted:
        session.flash = '%s created!' % table._singular
        redirect(URL(request.controller, 'list'))
    elif form.errors:
        response.flash = 'Please correct the errors'

    response.view = 'template/create.html'
    return dict(item_name=table._singular, form=form)


def view():
    item = table(table.id == request.args(0)) or redirect(URL('index'))
    form = SQLFORM(table, item, readonly=True, comments=False)

    response.view = 'template/view.%s' % request.extension
    return dict(item_name=table._singular, form=form, item=item)


@auth.requires_login()
def edit():
    # db.support_case.case_subcategory.requires = IS_IN_DB(
    #     # db, db.case_subcategory._id, db.case_category._format,
    #     db, db.case_subcategory._id, '%(case_category)s*%(title)s',
    #     # sort=True,  # orderby=db.case_subcategory.title,
    #     # cache=(cache.ram, 60)
    # )

    item = table(request.args(0)) or redirect(URL('index'))
    form = SQLFORM(table, item)

    if form.process().accepted:
        session.flash = '%s updated!' % table._singular
        redirect(URL(request.controller, 'list'))
    elif form.errors:
        response.flash = 'Please correct the errors'

    response.view = 'template/edit.html'
    return dict(item_name=table._singular, form=form)


@auth.requires_membership('admin')
def populate():
    query = table
    set = db(query)
    # rows = set.select()
    set.delete()
    from gluon.contrib.populate import populate
    populate(table, 15)
    redirect(URL('list'))


@auth.requires_membership('admin')
def update():
    query = table
    set = db(query)
    rows = set.select()

    for row in rows:
        # row.xxxx = 'yyyy'
        row.update_record()

    redirect(URL('list'))
