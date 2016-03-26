# -*- coding: utf-8 -*-

#########################################################################
# Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web', SPAN(2), 'py'), XML('&trade;&nbsp;'),
                  _class="navbar-brand", _href="http://www.web2py.com/",
                  _id="web2py-logo")

# default page title that appears in browser tabs and bookmarks
response.title = '%s: %s %s' % (
    request.application.replace('_', ' ').title(),
    request.controller.replace('_', ' ').title(),
    request.function.replace('_', ' ').title()
)

response.subtitle = ''

# default view title that appears at top of default layout content section
response.view_title = '%s %s' % (
    request.controller.replace('_', ' ').title(),
    request.function.replace('_', ' ').title()
)

# read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

response.company = myconf.get('app.company')
response.version = myconf.get('app.version')

# your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
# this is the main application menu add/remove items as required
#########################################################################

# todo - use response menu in layout.html


def menu_item(label, controller, action, icon='link', args=[], user_signature=False, submenu=[]):
    link = URL(controller, action, args=args, user_signature=user_signature)
    menu_item = ((I(' ', _class='fa fa-%s' % icon), T(label)), link == URL(), link, submenu)
    return menu_item


response.menu = [
    menu_item('Home', 'default', 'index', icon='home'),
    menu_item('People', 'person', 'list', icon='home'),
    menu_item('Dogs', 'dog', 'list', icon='home'),
    menu_item('Dog Owners', 'dog_owner', 'list', icon='home'),
]
