# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
from plugin_haystack import Haystack

def search():
    Posts = None
    if request.args(0) is not None:
        query = MyIndex.search(PostedBy = request.args(0))
        Posts = db(query).select()
    else:
        Posts = db().select(db.Posts.ALL)
    return dict(Posts = Posts)

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    Posts = None
    if request.args(0) is not None:
        query = index.search(request.args(0))
        Posts = db(query).select()
    else:
        Posts = db().select(db.Posts.ALL)
    return dict(Posts = Posts)

def Lookbook():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    Posts = None
    if auth.user is not None:
        Posts = db(db.Posts.PostedBy == auth.user.username).select()

    return dict(Posts = Posts)

def add():
    form = SQLFORM(db.Posts,upload=URL('download'))
    if form.process().accepted:
        session.flash = T("Post added")
        redirect(URL('default','index'))
    elif form.errors:
        session.flash = T('Please correct the info')
    return dict(form = form)



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
    http://..../[app]/default/user/verify_email
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@auth.requires_login()
@auth.requires_signature()
def delete():
    if request.args(0) is not None:
        q = ((db.Posts.PostedBy == auth.user.username) & (db.Posts.id == request.args(0)))
        db(q).delete()
    redirect(URL('default', 'index'))

@auth.requires_login()
def edit():
    """
    - "/edit/3" it offers a form to edit a checklist.
    'edit' is the controller (this function)
    '3' is request.args[0]
    """
    if request.args(0) is None:
        # We send you back to the general index.
        redirect(URL('default', 'index'))
    else:
        q = ((db.Posts.PostedBy == auth.user.username) &
             (db.Posts.id == request.args(0)))
        # I fish out the first element of the query, if there is one, otherwise None.
        cl = db(q).select().first()
        if cl is None:
            session.flash = T('Not Authorized')
            redirect(URL('default', 'index'))
        # Always write invariants in your code.
        # Here, the invariant is that the checklist is known to exist.
        # Is this an edit form?
        form = SQLFORM(db.Posts)
    return dict(form=form)


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

def profile():
    return dict(form=auth())

def get_posts():
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    posts = []
    has_more = False
    rows = db().select(db.Posts.ALL, limitby=(start_idx, end_idx + 1))
    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            t = dict(
                Picture = r.Picture,
                MyMessage = r.MyMessage,
                PostedBy = r.PostedBy,
                CreatedOn = r.CreatedOn.strftime("%B %d, %Y"),
                Likes = r.Likes,
                Dislikes = r.Dislikes,
                Shopping = r.Shopping,
                Tags = r.tags
            )
            posts.append(t)
        else:
            has_more = True
    logged_in = auth.user is not None
    user = None;
    if auth.user is not None:
        user = auth.user.username
    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,
        user=user
    ))
