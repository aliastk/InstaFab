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

def GetUserID():
    return auth.user.username if auth.user is not None else None


db.define_table('Posts',
                Field('Picture','upload'),
                Field('MyMessage', 'text'),
                Field('PostedBy','text',writable = False,default = GetUserID()),
                Field('CreatedOn', 'datetime',writable= False, readable = False, default = datetime.datetime.utcnow()),
                Field('Likes','integer',writable=False,readable=False,default = 0),
                Field('Dislikes','integer',writable=False,readable=False,default = 0),
                Field('Shopping','text')
                )
