# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
 
    
    return dict(page_title="library",message=T('Welcome to web2py!'),user=session.user)
def search():
    advanced_search = SQLFORM(db.advanced_search)
    databases = []
    if advanced_search.process(dbio=False).accepted:
        
        part_string = splitting(advanced_search.vars["author"])
        last_price = advanced_search.vars["price"]
        last_book = splitting(advanced_search.vars["book"])
        last_publisher = splitting(advanced_search.vars["publisher"])
        last_year = advanced_search.vars["year"]
        last_category = splitting(advanced_search.vars["category"])
        last_book_info = db(db.books.title==last_book).select()
      
        if part_string != "":
            databases.append(db.books.author_name == part_string )
        if last_price != "":
            databases.append(db.books.price == last_price)
        if last_book != "":
            databases.append(db.books.title == last_book )
        if last_publisher != "":
            databases.append(db.books.publisher == last_publisher)
        if last_year != "":
            databases.append(db.books.year == last_year )
        if last_category != "":
            databases.append(db.books.category == last_category)
        query = reduce(lambda a,b:(a&b),databases)
        database_function_info = db(query).select()
    else:
        database_function_info = []
        
    return dict(page_title="Modern Library", advanced_search=advanced_search, database_function_info=database_function_info)
def erase_last_whitespace(name):
    if (len(name)):
      while(name[-1]==" "):
         name = name[:-1] + name[-1].replace(" ", "")
    else:
         name = None    
    return name
def splitting(name):
    name = name.lower()
    words = name.split(" ")
    name_changer = [word.capitalize() for word in words]
    whole_name = ""
    for i in name_changer:
        
	    if(i!=""):
	       whole_name = whole_name + i + " "
    if whole_name != "": 
        whole_name = erase_last_whitespace(whole_name)
    return whole_name
def edit_comment():
    global user
    form = FORM("Your comment", BR(), 
              TEXTAREA(_name='comment', _cols= 40, _rows=5, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _value="SEND COMMENT"))
    form_id = request.args(1)
    form_update = None
    category = request.args(0)
    image_id = request.args(2)
    account_id = request.vars['q']
    rows = db(db.post.id == form_id).select()
    if (session.user and session.user.id == account_id):
       #account = user
       account = db.user(account_id)
       
    else:   
       account = db.user(account_id)
    if form.process().accepted:
         rows = db(db.post.id == form_id).select().first()
         rows.update_record(body = form.vars.comment)
         redirect(URL(category, args=[image_id]))
    return dict(page_title="Edit Comment", form=form, form_update=rows, account_id=account_id, account = account)         
def delete_comment():
    global user
    form = FORM("Delete The Comment", BR(), 
              
              INPUT(_type='submit', _value="DELETE COMMENT"))
    form_id = request.args(1)
    form_update = None
    category = request.args(0)
    image_id = request.args(2)
    account_id = request.vars['q']
    
    if (session.user and session.user.id == account_id):
       #account = user
       account = db.user(account_id)
       
    else:   
       account = db.user(account_id)
    if form.process().accepted:
         db(db.post.id == form_id).delete()
         redirect(URL("default", category, args=[image_id]))
    return dict(page_title="Delete Comment", form=form, account_id=account_id, account = account)    
def author():
    authors_data = db().select(db.authors.ALL, orderby=db.authors.name)    
    book_data = db().select(db.books.ALL, orderby=db.books.title)
	
    k = int(request.args[1])
    author_obj = None
	
	
    for author in authors_data:
      if k == author["id"]:
         author_obj = author
         break
	
    books = []
	
    for book in book_data:
      if k == book["author"]:
         books.append(book)
    
    if author_obj == None:
       # raise HTTP(404, 'Page not found', test='hello') 
       redirect(URL("error_page", vars=dict(url=request.env.path_info)))    
    return dict(page_title=author_obj["name"], author=author_obj, books=books, id=k)
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
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

def authors():
    authors_list = db().select(db.authors.ALL, orderby=db.authors.name)
    authors = dict()
    books = db().select(db.books.ALL, orderby=db.books.title)
    for book in books:
        author_obj = find_author(book)
        author_name = author_obj["name"]
        if author_name in authors:
          authors[author_name] = (authors[author_name][0]+1, author_obj['id'])
        else:   
          authors[author_name] = (1, author_obj['id'])

def find_author(book):
    authors_data = db().select(db.authors.ALL, orderby=db.authors.name)
    for author in authors_data:
     if book["author"] == author["id"]:
       return author
    return None
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

def find_au():
    row = db(db.authors.id==request.args.qw).select().first()
    name = row.name
    return str(name)

def find_auth(auth_id):
    row = db(db.authors.id==auth_id).select().first()
    name = row.name
    return name

def books():
    p1=0
    book = db.books(request.args(0,cast=int)) or redirect(URL('index'))
    u = db((db.post.image_id==int(book.id))).select()
    for l in u:
        p1=p1+1
    print p1
    image_id = request.args(0,cast=int)
    db.books.id.default = book.id
    db.post.image_id.default = book.id
    category_field = request.function
    if session.user != None:
        pid=request.vars["p"]
        print pid
        if pid:
            m = db((db.post.author == int(session.user.id)) & (db.post.image_id==int(book.id))).select().first()
            if m.star==None:
                pr=1
            else:
                pr=0
                l=float(m.star)
            m.update_record(star = pid)
            print session.user.id
            
            print "satyam"
            print session.user.id
            print int(book.id)
            
            print m.star
            
            print "he"
            print pr
            if pr:
                if db.books[book.id].rating:
                    t=float(db.books[book.id].rating)
                else:
                    t=0
                db.books[book.id].update_record(rating=((int(p1)-1)*float(t)+float(pid))/(int(p1)))
            else:
                t=float(db.books[book.id].rating)
                p1=int(p1)
                db.books[book.id].update_record(rating=(p1*t-l+float(pid))/p1)
                print (l+float(pid))/2
            
        form = FORM("Your comment", BR(), 
              TEXTAREA(_name='comment', _cols= 40, _rows=5, requires=IS_NOT_EMPTY()),
              INPUT(_type='submit', _value="SEND COMMENT"))
        if form.process().accepted:
          db.post.insert(image_id=image_id, 
                         author=session.user,
                         field=category_field,
                         body = form.vars.comment
                        )
          response.flash = 'your comment is posted. Click to exit'
    else: 
        form = None 
    comments = db( (db.post.image_id==book.id) & (db.post.field==category_field) &
                   (db.post.author == db.user.id)).select()
    book_info = db(db.books.id == book.id).select()
    authr = find_auth(book.author);
    book = db.books(request.args(0,cast=int)) or redirect(URL('index'))
    return dict(page_title=book.title + (" (%dTL)" % book.price), book_info=book_info, book=book, form=form, comments=comments , author=authr)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
def account():
    account_id = request.args(0,cast=int)
    age = ""
    users = db().select(db.authors.ALL)
    admin = db(db.user.role == "admin").select().first()
    if admin:
        admin_id = admin.id
    else:
        admin_id=-1
    user=session.user   
    if (user and (user.id == account_id or user.id == admin_id)):
       #account = user
       account = db.user(account_id)
       form = FORM(
          
          'Password', INPUT(_name='pw1', _type='password', label='Password', requires=IS_NOT_EMPTY()), BR(),
          'Password2', INPUT(_name='pw2', _type='password', label='Confirm password',
           requires=[IS_NOT_EMPTY(),IS_EQUAL_TO(request.vars.pw1, "don't match")]), BR(),
          
          'Age', INPUT(_name='age', requires=IS_INT_IN_RANGE(0,100)), BR(),
          'City', INPUT(_name='city'), BR(),
          'Information', TEXTAREA(_name='info', _cols= 40, _rows=5),
           INPUT(_type='submit', _value="UPDATE ACCOUNT"),
           _id="loginform", _class="bootstrapform"
       )
       user_db = db(db.user.id == account_id).select()
       if form.process().accepted:
           for person in user_db:
               person.update_record(
                                    password = encyrpted(form.vars.pw1),
                                    password2 = encyrpted(form.vars.pw2),
                                    city = form.vars.city,
                                    age = form.vars.age,
                                    information = form.vars.info,
                                    )
           redirect(URL("account", args=[account_id]))
          
    else:   
       account = db.user(account_id)
       form = None
       if account == None:
           redirect(URL('index'))
    return dict(page_title="Account",account=account, form=form,user=session.user)

def bookdisplay():
    id=request.vars.id
    if not id:
        id=-1
    else:
        id=int(id)-1
        id=c[int(id)]
    return dict(page_title="Books",id=str(id))
def authors():
    authors_list = db().select(db.authors.ALL, orderby=db.authors.name)
    authors = dict()
    books = db().select(db.books.ALL, orderby=db.books.title)
    for book in books:
        author_obj = find_author(book)
        author_name = author_obj["name"]
        if author_name in authors:
          authors[author_name] = (authors[author_name][0]+1, author_obj['id'])
        else:   
          authors[author_name] = (1, author_obj['id'])
    return dict(page_title="Authors", authors_list = authors_list, books=books, authors=authors)
