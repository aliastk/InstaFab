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
from plugin_haystack import Haystack,WhooshBackend

def GetUserID():
    return auth.user.username if auth.user is not None else None


db.define_table('Posts',
                Field('Picture','upload'),
                Field('MyMessage', 'text'),
                Field('PostedBy','text',writable = False,default = GetUserID()),
                Field('CreatedOn', 'datetime',writable= False, readable = False, default = datetime.datetime.utcnow()),
                Field('Likes','integer',writable=False,readable=False,default = 0),
                Field('Dislikes','integer',writable=False,readable=False,default = 0),
                Field('Shopping','text'),
                Field('Tags','string' , default="all", required=True),
                Field('Archived','boolean',default=False,writable=False,readable=False)
                )


db.executesql('CREATE INDEX IF NOT EXISTS mytagx ON Posts (Tags);')
db.executesql('CREATE INDEX IF NOT EXISTS myPosterx ON Posts (PostedBy);')
MyIndex = Haystack(db.Posts)
MyIndex.indexes('PostedBy','Tags')
    #writer = MyIndex.backend.ix.writer()
    #if post.Archived is False:
    #writer.add_document(id=unicode(post.id),PostedBy=unicode(post.PostedBy),Tags=unicode(post.Tags))
    #post.Archived = True
    #post.update_record()
    #writer.commit()
