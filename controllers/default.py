# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import datetime
from dateutil import relativedelta
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
    #Posts = db().select(db.Posts.ALL)
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
    Posts = None
    #Posts = db().select(db.Posts.ALL)
    return dict(Posts = Posts)

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

def favorite():
    # TODO: Find the user and update the favorite list
    print "called"
    print type(request.vars.id)
    print auth.user
    row = db(db.Favorites.ListOwner == auth.user).select().first()
    print type(row)
    if(row is None):
        db.Favorites.insert(ListOwner = auth.user,
                            FavoritesList = [int(request.vars.id)])
        print "none"
    else:
        favorites = row.FavoritesList
        if(int(request.vars.id) in row.FavoritesList):
            print "found"
            row.FavoritesList.remove(int(request.vars.id))
        else:
            print "not found"
            row.FavoritesList.append(int(request.vars.id))
        row.update_record()

    return

def LikeOrDislike():
    #true is upvote, false is downvote
    id = int(request.vars.id)
    if(request.vars.vote is None):
        return "no vote"
    vote = request.vars.vote == 'true'
    check = db((db.Vote.Voter == auth.user) & (db.Vote.Post == id)).select(limitby=(0,1)).first();
    if (check is not None):
        check.UpVote = vote
        check.update_record()
        if vote:
            check.Post.Likes+=1
            check.Post.Dislikes-=1
        else:
            check.Post.Dislikes+=1
            check.Post.Likes-=1
    else:
        check = db.Vote.insert(
            Voter = auth.user,
            Post = id,
            UpVote = vote
        )
        check = db.Vote(check)
        print check
        if vote:
            check.Post.Likes+=1
        elif(vote == False):
            check.Post.Dislikes+=1

    if(vote):
        check.Post.rating +=1
        check.Post.search_rating +1
    elif(vote == False):
        check.Post.rating -=1
        check.Post.search_rating -=1

    check.Post.update_record()
    return response.json(dict(
        vote = check.UpVote
    ))

def get_posts():
        start_idx = int(request.vars.start_idx) if request.vars.start_idx is not None else 0
        end_idx = int(request.vars.end_idx) if request.vars.end_idx is not None else 0
        search = request.vars.search
        who = request.vars.who if request.vars.who is not None else None
        viewFavorites = request.vars.viewFavorites if request.vars.viewFavorites is not None else False
        logged_in = auth.user is not None
        user = None
        query = db.Posts._id>0
        searching = False

        if auth.user is not None:
            user = auth.user.username

        if(who=="true"):
            query = query & (db.Posts.PostedBy==auth.user.username)
            searching = True

        favorites = []

        if(logged_in):
            GetFavorites = db(db.Favorites.ListOwner == auth.user).select().first()
            if(GetFavorites != None):
                favorites = GetFavorites.FavoritesList

        if(viewFavorites=="true"):
            query = query & db.Posts._id.belongs(favorites)

        if ((search is not None) and (len(search)>0)):
            query = query & MyIndex.search(Tags=search)
            searching = True;
        return get_posts_handler(query,favorites,start_idx,end_idx,logged_in,searching,user)

def get_posts_handler(query,favorites,start_idx,end_idx,logged_in,searching,user):
    from math import exp
    # return Get_Favorites();

    if(searching):
        rows = db(query).select(orderby=~db.Posts.search_rating)
    else:
        rows = db(query).select(orderby=~db.Posts.rating)

    favorites = set(favorites)
    today = datetime.datetime.utcnow()
    posts = []
    has_more = False

    for i, r in enumerate(rows):
        print r
        if i < end_idx-start_idx:
            if(r.id in favorites):
                favorited = True
            else:
                favorited = False

            vote = None
            if logged_in:
                vote = db((db.Vote.Voter == auth.user) & (db.Vote.Post == r.id)).select(limitby=(0,1)).first();
                if vote:
                    vote = vote.UpVote

            t = dict(
                #Picture = URL('default','download',args=r.Picture),
                Picture = r.PictureUrl,
                MyMessage = r.MyMessage,
                PostedBy = r.PostedBy,
                CreatedOn = r.CreatedOn.strftime("%B %d, %Y"),
                Likes = r.Likes,
                edit = False,
                voted = vote,
                id = r.id,
                Shopping = r.Shopping,
                Dislikes = r.Dislikes,
                Tags = filter(None,r.Tags.split("#")),
                FullTag = r.Tags,
                favorited = favorited
            )


            if(searching and logged_in and r.PostedBy is not auth.user.username):
                timediff = datetime.datetime.now() - r.search_recency
                timediff = timediff.total_seconds()/60
                r.search_rating = r.search_rating*exp(-1*timediff)
                r.search_recency = datetime.datetime.now()
            elif(not searching):
                timediff = datetime.datetime.now() - r.Recency
                timediff = timediff.total_seconds()/60
                r.rating = r.rating*exp(-1*timediff)
                r.Recency = datetime.datetime.now()

            r.update_record()

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
