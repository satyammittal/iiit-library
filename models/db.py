db = DAL("sqlite://storage.sqlite")
db.define_table('authors',
                Field('id', 'integer'),
                Field('name', unique=True),
                Field('bio',length=1000000),
                Field('file', 'upload')
                )
db.define_table('post',
                Field('id', 'integer'),
                Field('image_id', 'integer'),
                Field('field'),
                Field('author', 'integer'),
                Field('star','float'),
                Field('email'),
                Field('age'),
                Field('body', 'text'))
db.define_table('advanced_search',
                Field('author'),
                Field('book'),
                Field('category'),
                Field('year'),
                Field('price'),
                Field('publisher')
                )
db.define_table('user',
  Field('id'),
  Field('username', unique=True, required=True),
  Field('password', 'password', required=True),
  Field('roll_number','integer',required=True),
  Field('photo','upload'),
  Field('role'),
  Field('email'),
  Field('age', 'integer'),
  Field('city'),
  Field('information', length="100000"),
  Field('login_time', 'integer') 
)
db.user.email.requires = IS_EMAIL()
#db.post.image_id.requires = IS_IN_DB(db, db.books.id, '%(title)s')
db.post.author.requires = IS_NOT_EMPTY()
db.post.email.requires = IS_EMAIL()
db.user.email.requires= IS_NOT_IN_DB(db, db.user.email)
db.post.body.requires = IS_NOT_EMPTY()

db.post.image_id.writable = db.post.image_id.readable = False
db.define_table('books',
                Field('author','integer', 'reference authors.id'),
                Field('author_name','string' ),
                Field('title', unique=True),
                Field('category'),
                Field('price', 'integer'),
                Field('year', 'integer'),
                Field('publisher' , 'string'),
                Field('amazon_link', length=1000),
                Field('betterworld_link', length=1000),
                Field('idefix_link', length=1000),
                Field('id', 'integer', 'compute'),
                Field('file', 'upload'),
                Field('info','string', length=10000),
               Field('total_copies','integer'),
               Field('available','integer'),
               Field('rating','float',default=0))
if session.user:
  user = session.user
else:
  user = None
c=["Classic","Science Fiction","Romance","Adventure","Thrill","History","Engineering","Others"]
p1=0
