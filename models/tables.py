# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.




# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
import datetime
import time
from plugin_haystack import Haystack,WhooshBackend

def GetUserID():
    return auth.user.username if auth.user is not None else None



db.define_table('Posts',
                Field('PictureUrl','text'),
                Field('MyMessage', 'text'),
                Field('PostedBy','text',writable = False,default = GetUserID()),
                Field('CreatedOn', 'datetime',writable= False, readable = False),
                Field('Likes','integer',writable=False,readable=False,default = 0),
                Field('Dislikes','integer',writable=False,readable=False,default = 0),
                Field('Tags','string' , default="all", required=True),
                Field('rating','float'),
                Field('search_rating','float'),
                Field('search_recency','datetime'),
                Field('Recency','datetime'),
                Field('Shopping','text')
                )



db.define_table('Favorites',
                Field('ListOwner','reference auth_user'),
                Field('FavoritesList','list:reference Posts')
               )

db.define_table('Vote',
                Field('Voter','reference auth_user'),
                Field('Post','reference Posts'),
                Field('UpVote','boolean')
               )

MyIndex = Haystack(db.Posts)
MyIndex.indexes('PostedBy','Tags')
    #writer = MyIndex.backend.ix.writer()
    #if post.Archived is False:
    #writer.add_document(id=unicode(post.id),PostedBy=unicode(post.PostedBy),Tags=unicode(post.Tags))
    #post.Archived = True
    #post.update_record()
    #writer.commit()
