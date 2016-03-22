# -*- coding: utf-8 -*-


class Titleize(object):
    '''Field(..., requires=Titleize())'''

    def __call__(self, value):
        return (value.title(), None)


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
