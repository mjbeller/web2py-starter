from gluon import *

'''
maintain list of breadcrumbs in session

at top of controller:
    breadcrumbs.append('dashboard', '{} {}'.format(
        'Home',
        request.function.replace('_', ' ').title(),
    ))
or
    breadcrumbs.append('dashboard', response.view_title)

in view, e.g., layout.html:

  <ol class="breadcrumb">
    {{for crumb in session.breadcrumbs:}}
      <li><a href="{{=crumb[0]}}"><i class="fa fa-{{=crumb[1]}}"></i> {{=crumb[2]}}</a></li>
    {{pass}}
  </ol>

 icon name can be any fontawesome icon name, e.g.:
    fa-dashboard, list, pencil-square-o,

this could be defaults for app:
'''

def get_context_icon():
    context_icons = {
        'context': {
            'borrower': 'building-o',
            'investor': 'university',
            'deal': 'suitcase',
            'participant': 'university',
            'content': 'file-text-o',
        },
        'tools': {
            'message': 'envelope-o',
            'notification': 'bell-o',
            'task': 'flag-o',
            'favorite': 'heart',
        },
        'function': {
            'dashboard': 'dashboard',
            'list': 'list',
            'create': 'pencil-square-o',
            'view': 'search',
            'edit': 'pencil-square-o',
        },
        'home': {
            'index': 'home',
            'about': 'book',
            'tou': 'book',
            'privacy': 'book',
        },
        'appadmin': {
            'appadmin': 'gears',
            'content': 'file-text-o',
            'users': 'users',
            'db': 'database',
            'auth': 'wrench',
        },
    }

    controller = current.request.controller
    function = current.request.function
    args = current.request.args

    if controller in context_icons['context']:
        return context_icons['context'][controller]
    elif function in context_icons['function']:
        return context_icons['function'][function]
    elif controller == 'default' and function in context_icons['home']:
        return context_icons['home'][function]
    elif controller == 'appadmin' and args and args[0] in context_icons['appadmin']:
        return context_icons['appadmin'][args[0]]
    elif controller == 'appadmin':
        return context_icons['appadmin']['appadmin']
    else:
        return 'bookmark'


def append(icon=None, label=None, url=None):

    current.session.breadcrumbs = current.session.breadcrumbs or []
    breadcrumbs = current.session.breadcrumbs

    controller = current.request.controller
    function = current.request.function
    args = current.request.args
    vars = current.request.vars

    url = url or URL(c=controller, f=function, args=args, vars=vars)
    icon = get_context_icon()

    if not label and controller == 'default':
        label = 'Home' if function == 'index' else function.replace('_', ' ').title()
    elif not label and controller == 'appadmin' and args:
        label = '{} {}'.format(
            'Manage',
            current.request.args[0].replace('_', ' ').title()
        )
    elif not label and controller == 'appadmin':
        label = 'Administration'
    else:
        label = current.response.view_title
        # label = '{} {}'.format(
        #     current.request.controller.replace('_', ' ').title(),
        #     current.request.function.replace('_', ' ').title()
        # )

    if not breadcrumbs or breadcrumbs[-1]['label'] != label:
        crumb = {'url': url, 'icon': icon, 'label': label}
        breadcrumbs.append(crumb)

    if len(breadcrumbs) > 3:
        del breadcrumbs[0]

    return
