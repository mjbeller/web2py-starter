# -*- coding: utf-8 -*-

from gluon.sqlhtml import FormWidget

# dal represent/format helpers
## https://mkaz.tech/python-string-format.html
## https://pyformat.info/#number


def dal_represent_number(v, r):
    return "{:,}".format(v) if v is not None else v


def dal_represent_percent(v, r):
    return "{:.2%}".format(v / 100) if v is not None else v


# https://regex101.com/
# http://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number
dal_regex_phone_num = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'
dal_regex_na_phone_num = '^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$'
dal_regex_ssn = '^\d{3}-\d{2}-\d{4}$'

dal_list_genders = [('F', 'Female'), ('M', 'Male')]
dal_list_booleans = [('Y', 'Yes'), ('N', 'No')]

dal_list_states = [
    ('AL', 'Alabama, USA'),
    ('AK', 'Alaska, USA'),
    ('AB', 'Alberta, CAN'),
    ('AS', 'American Samoa, USA'),
    ('AZ', 'Arizona, USA'),
    ('AR', 'Arkansas, USA'),
    ('BC', 'British Columbia, CAN'),
    ('CA', 'California, USA'),
    ('CO', 'Colorado, USA'),
    ('CT', 'Connecticut, USA'),
    ('DE', 'Delaware, USA'),
    ('FL', 'Florida, USA'),
    ('GA', 'Georgia, USA'),
    ('GU', 'Guam, USA'),
    ('HI', 'Hawaii, USA'),
    ('ID', 'Idaho, USA'),
    ('IL', 'Illinois, USA'),
    ('IN', 'Indiana, USA'),
    ('IA', 'Iowa, USA'),
    ('KS', 'Kansas, USA'),
    ('KY', 'Kentucky, USA'),
    ('LA', 'Louisiana, USA'),
    ('ME', 'Maine, USA'),
    ('MB', 'Manitoba, CAN'),
    ('MD', 'Maryland, USA'),
    ('MA', 'Massachusetts, USA'),
    ('MI', 'Michigan, USA'),
    ('MN', 'Minnesota, USA'),
    ('MS', 'Mississippi, USA'),
    ('MO', 'Missouri, USA'),
    ('MT', 'Montana, USA'),
    ('NE', 'Nebraska, USA'),
    ('NV', 'Nevada, USA'),
    ('NB', 'New Brunswick, CAN'),
    ('NH', 'New Hampshire, USA'),
    ('NJ', 'New Jersey, USA'),
    ('NM', 'New Mexico, USA'),
    ('NY', 'New York, USA'),
    ('NL', 'Newfoundland and Labrador, CAN'),
    ('NC', 'North Carolina, USA'),
    ('ND', 'North Dakota, USA'),
    ('MP', 'Northern Mariana Islands, USA'),
    ('NT', 'Northwest Territories, CAN'),
    ('NS', 'Nova Scotia, CAN'),
    ('NU', 'Nunavut, CAN'),
    ('OH', 'Ohio, USA'),
    ('OK', 'Oklahoma, USA'),
    ('ON', 'Ontario, CAN'),
    ('OR', 'Oregon, USA'),
    ('PA', 'Pennsylvania, USA'),
    ('PE', 'Prince Edward Island, CAN'),
    ('PR', 'Puerto Rico, USA'),
    ('QC', 'Quebec, CAN'),
    ('RI', 'Rhode Island, USA'),
    ('SK', 'Saskatchewan, CAN'),
    ('SC', 'South Carolina, USA'),
    ('SD', 'South Dakota, USA'),
    ('TN', 'Tennessee, USA'),
    ('TX', 'Texas, USA'),
    ('VI', 'U.S. Virgin Islands, USA'),
    ('UT', 'Utah, USA'),
    ('VT', 'Vermont, USA'),
    ('VA', 'Virginia, USA'),
    ('WA', 'Washington, USA'),
    ('DC', 'Washington DC, USA'),
    ('WV', 'West Virginia, USA'),
    ('WI', 'Wisconsin, USA'),
    ('WY', 'Wyoming, USA'),
    ('YT', 'Yukon Territory, CAN'),
]


class Titleize(object):
    '''Field(..., requires=Titleize())'''

    def __call__(self, value):
        # return (value.title(), None)
        articles = ('in', 'the', 'a', 'an', 'of', 'is')
        return (' '.join([w if w in articles else w.title() if w.islower() else w for w in value.split()]), None)


# custom forms
# https://groups.google.com/d/msg/web2py/1yCGgKANssE/MvOL4mUqRQ4J


def widget(type='string', placeholder=''):
    '''Allow Field('name', widget=widget('string', 'my placeholder text'))'''
    # https://groups.google.com/d/msg/web2py/CTsUjEFUcR4/Vy-wIekEBAAJ
    # could also do https://groups.google.com/d/msg/web2py/VSr2oLNnozg/5AlMTNzdGgkJ
    return lambda field, value: SQLFORM.widgets[type].widget(field, value, _placeholder=placeholder)


def mcg_date_widget(field, value):
    return INPUT(_name=field.name,
                 _id="%s_%s" % (field._tablename, field.name),
                 _class='form-control ' + field.type,
                 _value=value,
                 data={
                     'date-format': 'mm/yyyy',
                     'date-min-view-mode': '1'
                 },
                 requires=field.requires)


def datepicker_widget(**settings):

    def widget(field, value, **attributes):

        default = {'value': value}

        attributes = FormWidget._attributes(field, default, **attributes)
        attributes['_class'] = 'form-control date'

        # default format “mm/dd/yyyy”

        data_attributes = {}
        data_attributes['date-format'] = 'yyyy-mm-dd'
        for item in settings.iteritems():
            data_attributes['date-'+item[0].replace('_', '-')] = item[1]

        return INPUT(
            data=data_attributes,
            **attributes
        )

    return widget


def sidebar_menu_item(label, url=None, icon='link'):
    '''
    <li><a href="{{=URL('default','about')}}"><i class="fa fa-book"></i> <span>About</span></a></li>
    <a href="#"><i class="fa fa-gears"></i> <span>Admin</span> <i class="fa fa-angle-left pull-right"></i></a>
    '''

    if url:
        active = 'active' if url == URL() else None
        return LI(
            A(
                (I(' ', _class='fa fa-%s' % icon), SPAN(T(label))),
                _href=url
            ),
            _class=active
        )
    else:
        return A(
            (
                I(' ', _class='fa fa-%s' % icon),
                SPAN(T(label)),
                I(' ', _class='fa fa-angle-left pull-right'),
            ),
            _href="#"
        )


# this is the main application menu add/remove items as required
# original response menu in layout.html
#
#
# def menu_item(label, controller, action, icon='link', args=[], user_signature=False, submenu=[]):
#     link = URL(controller, action, args=args, user_signature=user_signature)
#     menu_item = ((I(' ', _class='fa fa-%s' % icon), T(label)), link == URL(), link, submenu)
#     return menu_item
#
#
# response.menu = [
#     menu_item('Home', 'default', 'index', icon='home'),
#     menu_item('People', 'person', 'list', icon='home'),
#     menu_item('Dogs', 'dog', 'list', icon='home'),
#     menu_item('Dog Owners', 'dog_owner', 'list', icon='home'),
# ]


def is_user_member(*roles):
    # @auth.requires(lambda: is_user_member('arg', 'list', 'of', 'roles')
    # if is_user_member('arg', 'list', 'of', 'roles'):

    # @auth.requires(lambda: any([auth.has_membership(r) for r in ['list', 'of', 'roles'])) # db lookups!?
    # if auth.user and any(auth.has_membership(r) for r in ['customer_service', 'admin']): # performs potentially 4 database queries
    # if auth.has_membership('customer_service'): # performs two database
    # restrict menu options based on membership
    # https://groups.google.com/d/msg/web2py/bz-mKIFqP1w/eEma0XOyCAAJ
    # https://groups.google.com/forum/#!searchin/web2py/response.menu$20auth.user_id$20auth.has_membership/web2py/E8Krnt9cxB8/xSpuPy8d6M4J
    # https://groups.google.com/forum/#!searchin/web2py/response.menu$20auth.user_id$20auth.has_membership/web2py/GvDAXRIpKA0/sEcPeB8a40oJ
    # https://groups.google.com/forum/#!topic/web2py/8AHYqV_EKy0

    user_auth_groups = [x.lower() for x in auth.user_groups.values()]
    required_auth_groups = [x.lower() for x in roles]

    if auth.user and any(role in required_auth_groups for role in user_auth_groups):
        return True
    else:
        return False


def user_visibility(*groups):
    """in views, in class attribute: {{=user_visibility('list', 'of', 'authorized', 'user_groups')}}"""
    return 'hidden' if not is_user_member(*groups) else 'visible'
