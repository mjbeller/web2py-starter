# -*- coding: utf-8 -*-

from bookmark import Bookmark


def add():

    Bookmark.from_dict(request.vars['bookmark_obj']).add()

    # bookmark, bookmarks = get_bookmark()
    #
    # # update session and db
    # if bookmark['key'] not in bookmarks:
    #     bookmarks[bookmark['key']] = bookmark['data']
    #     db(db.auth_user.id == auth.user.id).update(bookmarks=bookmarks)

    # redirect(URL('default', 'index'))
    return


def delete():

    Bookmark.from_dict(request.vars['bookmark_obj']).delete()

    # bookmark, bookmarks = get_bookmark()
    #
    # # update session and db
    # try:
    #     del bookmarks[bookmark['key']]
    #     db(db.auth_user.id == auth.user.id).update(bookmarks=bookmarks)
    # except:
    #     pass

    # redirect(URL('default', 'index'))
    return


# def get_bookmark():
#
#     import ast
#
#     bookmark = ast.literal_eval(request.vars['bookmark_obj'])
#
#     if not auth.user.bookmarks:
#         auth.user.bookmarks = {}
#     elif not isinstance(auth.user.bookmarks, dict):
#         auth.user.bookmarks = ast.literal_eval(auth.user.bookmarks)
#
#     bookmarks = auth.user.bookmarks
#
#     return bookmark, bookmarks


def list():

    response.view = 'bookmark/bookmark_list.html'
    return {}
