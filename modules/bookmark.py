# -*- coding: utf-8 -*-

# http://web2py.com/books/default/chapter/29/04/the-core#Sharing-the-global-scope-with-modules-using-the-current-object
from gluon import *

'''
Bookmarks are stored in db.auth_user and
    auth.user.bookmarks (as a dict) for easy access during a session

# Class methods:
- from_dict() returns an instance from a bookmark dict (see dict() below)
- list() returns a dict of bookmarks
    Sample k, v in Bookmarks:
    {
        'investor/list': {'i': None, 'c': 'investor', 'u': '/mcg/investor/list', 't': 'List Investor', 'f': 'list'}
    }

# Instance properties:
    key, label/title, controller, function, arg/id, url

# Instance methods:
- dict() a dict containing the key and bookmark data
    Sample Bookmark:
    {
        'key': 'investor/list',
        'data': {'i': None, 'c': 'investor', 'u': '/mcg/investor/list', 't': 'List Investor', 'f': 'list'}
    }
- add() and delete() adds or deletes the bookmark.dict()['key'] and ['data'] to auth.user.bookmarks and db.auth_user
- is_active() return 'active' if current URL matches bookmark


# Components:
- models/db1.py: bookmarks field added to auth_user table (see notes below on filter options)
- controllers/bookmark.py:
    - add function - add bookmark for user
    - delete function - delete bookmark for user
    - list function - return html with list of bookmarks for user
- views/layout.html:
    - bookmark.css
    - create Bookmark
    - display bookmark button
    - load bookmark list in sidebar
- views/web2py_ajax.html: bookmark.js
- views/bookmark/bookmark_button.html
- views/bookmark/bookmark_list.html
- static/js/bookmark.js
- static/css/bookmark.css
'''

'''
# bookmarks filter options
# http://web2py.com/books/default/chapter/29/06/the-database-abstraction-layer#filter_in-and-filter_out

# None!!  This ended up working best because web2py converts objects to and from their
# serialized representation (repr() or str()) automatically

# if bookmarks is any python object ...
import pickle
        filter_in = lambda bm_obj: pickle.dumps(bm_obj),
        filter_out = lambda bm_str: pickle.loads(bm_str) if bm_str else {},

# if bookmarks is any python literal ...
import ast
        filter_in = lambda bm_obj: repr(bm_obj),  # could be str()
        filter_out = lambda bm_str: eval(bm_str) if bm_str else {},  # could be ast.literal_eval

# if bookmarks is a python dict with valid json ... (appadmin does not use filter_in/out)
from simplejson import loads, dumps  # could be json vs. simplejson
        filter_in = lambda json_obj, dumps=dumps: dumps(json_obj),
        filter_out = lambda json_str, loads=loads: loads(json_str) if json_str else {}
'''

# def OLDcreate():
#     request = current.request
#     controller = current.request.controller
#     function = current.request.function
#     args = current.request.args
#     response = current.response
#
#     key = '{}/{}'.format(controller, function)
#     if args:
#         key = '{}/{}'.format(key, args[0])
#
#     url = URL()
#
#     # if not auth.user.bookmarks:
#     #     auth.user.bookmarks = {}
#     # elif not isinstance(auth.user.bookmarks, dict):
#     #     auth.user.bookmarks = ast.literal_eval(auth.user.bookmarks)
#
#     return {
#         'key': key,
#         'data': {
#             'c': request.controller,
#             'f': request.function,
#             'i': request.args[0] if request.args else None,
#             't': response.view_title,  # response.title,
#             'u': URL()
#         }
#     }
#
#
# def OLDis_active():
#
#     if auth.user and \
#         auth.user.bookmarks and \
#         response.bookmark['key'] in auth.user.bookmarks:
#
#         return 'active'
#
#     else:
#
#         return


class Bookmark(object):

    def __init__(
        self,
        t = None,  # label
        c = None,  # controller
        f = None,  # function
        i = None,  # id
        u = None  # url
    ):
        self.label = t or current.response.view_title
        self.controller = c or current.request.controller
        self.function = f or current.request.function
        self.arg = i or (current.request.args[0] if current.request.args else None)
        self.url = u or URL()

        # self.request = current.request
        # self.response = current.response
        # self.auth = current.auth

        key = '{}/{}'.format(self.controller, self.function)
        if self.arg:
            key = '{}/{}'.format(key, self.arg)

        self.key = key

    @classmethod
    def from_dict(cls, bookmark_dict):
        if isinstance(bookmark_dict, str):
            bookmark_dict = eval(bookmark_dict)

        return cls(
            t = bookmark_dict['data']['t'],
            c = bookmark_dict['data']['c'],
            f = bookmark_dict['data']['f'],
            i = bookmark_dict['data']['i'],
            u = bookmark_dict['data']['u'],
        )

    def dict(self):
        return {
            'key': self.key,
            'data': {
                't': self.label,
                'c': self.controller,
                'f': self.function,
                'i': self.arg,
                'u': self.url
            }
        }

    def __repr__(self):
        return repr(self.dict())

    def add(self):
        if not current.auth.user.bookmarks:
            current.auth.user.bookmarks = {}
        elif not isinstance(current.auth.user.bookmarks, dict):
            current.auth.user.bookmarks = eval(current.auth.user.bookmarks)

        if self.key not in Bookmark.list():
            current.auth.user.bookmarks[self.key] = self.dict()['data']
            query = (current.db.auth_user.id == current.auth.user.id)
            current.db(query).update(bookmarks=current.auth.user.bookmarks)

        return

    def delete(self):

        # appadmin and user/profile save bookmarks as str
        if not isinstance(current.auth.user.bookmarks, dict):
            current.auth.user.bookmarks = eval(current.auth.user.bookmarks)

        # update session and db
        try:
            del current.auth.user.bookmarks[self.key]
            query = (current.db.auth_user.id == current.auth.user.id)
            current.db(query).update(bookmarks=current.auth.user.bookmarks)
        except:
            pass

        return

    def is_active(self):
        '''returns 'active' if bookmark in bookmark list'''

        # if current.auth.user and \
        #     current.auth.user.bookmarks and \
        #     current.response.bookmark.dict()['key'] in Bookmark.list():
        #     # current.response.bookmark['key'] in current.auth.user.bookmarks:
        if self.key in Bookmark.list():
            return 'active'
        else:
            return

    @classmethod
    def list(cls):
        '''returns list of bookmarks as k,v pairs'''
        if not current.auth.user or not current.auth.user.bookmarks:
            return {}
        elif isinstance(current.auth.user.bookmarks, dict):
            return current.auth.user.bookmarks
        elif isinstance(current.auth.user.bookmarks, str):
            return eval(current.auth.user.bookmarks)
