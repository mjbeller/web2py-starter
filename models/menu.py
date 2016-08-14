# -*- coding: utf-8 -*-

#########################################################################
# Customize your APP title, subtitle and menus here
#########################################################################

response.logo_mini = IMG(_src=URL('static', 'images/favicon.png'), _alt=myconf.get('app.company'), _width="30px")

# response.logo = IMG(_src=URL('static', 'images/favicon.png'), _alt=myconf.get('app.company'), _width="180px")
# response.logo = SPAN('web', B(2), 'py', XML('&trade;&nbsp;'))
response.logo = myconf.get('app.abbreviation')

# default page title that appears in browser tabs and bookmarks
response.title = '%s: %s %s' % (
    myconf.get('app.abbreviation'),
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
