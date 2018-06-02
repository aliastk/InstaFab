# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
def test():
    Posts = None
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
    form = SQLFORM(db.Posts)
    if form.process().accepted:
        session.flash = T("Post added")
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

    # Here go your api methods.


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
    user = db(db.auth_user.username == request.args(0)).select()
    return dict(form=auth())

def edit_post():
    id = request.vars.id;

    return;

def delete_post():
    id = request.vars.id;
    db(db.Posts.id==id).delete();
    return;

def test_search():
    print MyIndex.search(Tags='green')
    return


def get_posts():

    # return Get_Favorites();
    start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
    end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
    search = request.vars.search
    posts = []
    has_more = False

    logged_in = auth.user is not None
    user = None;
    if auth.user is not None:
        user = auth.user.username

    if len(search)>0:
        query = MyIndex.search(Tags=search)
        rows = db(query).select()
    else:
        rows = db().select(db.Posts.ALL)

    favorites = []
    if(logged_in):
        GetFavorites = db(db.Favorites.ListOwner == auth.user).select().first()
        if(GetFavorites != None):
            favorites = GetFavorites.FavoritesList

    favorites = set(favorites)

    for i, r in enumerate(rows):
        if i < end_idx - start_idx:
            if(r.id in favorites):
                favorited = True
            else:
                favorited = False
            t = dict(
                #Picture = URL('default','download',args=r.Picture),
                Picture = r.PictureUrl,
                MyMessage = r.MyMessage,
                PostedBy = r.PostedBy,
                CreatedOn = r.CreatedOn.strftime("%B %d, %Y"),
                Likes = r.Likes,
                edit = False,
                id = r.id,
                Dislikes = r.Dislikes,
                Shopping = r.Shopping,
                Tags = filter(None,r.Tags.split("#")),
                FullTag = r.Tags,
                favorited = favorited
            )
            posts.append(t)
        else:
            has_more = True

    return response.json(dict(
        posts=posts,
        logged_in=logged_in,
        has_more=has_more,
        user=user,
        favorites = favorites
    ))
