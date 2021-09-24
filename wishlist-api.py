import flask
from flask import Flask, request,jsonify
import sqlite3
import sys

app=Flask(__name__)
app.debug=True

#This method used tp connect to sqllite database
def connect_db():
    print("inside connect_db") 
    conn=sqlite3.connect('wishlist.db')
    return conn

#This method will execute all DB scrips
def execute_script():
    print("inside execute_scripts")  
    try:
        conn=connect_db()
        cur=conn.cursor()   
        cur.execute("DROP TABLE IF EXISTS users")           
        cur.execute("""CREATE TABLE users (
                            userkey INTEGER PRIMARY KEY NOT NULL,
                            userid TEXT NOT NULL UNIQUE,
                            firstname TEXT NOT NULL,
                            lastname TEXT NOT NULL,
                            email  TEXT NOT NULL UNIQUE,
                            password  TEXT NOT NULL);""")

        print("users table script executed")           
        cur.execute("DROP TABLE IF EXISTS books")
        cur.execute('''
                    CREATE TABLE books(
                    bookkey INTEGER PRIMARY KEY NOT NULL,
                    ISBN TEXT  NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publishdate  TEXT NOT NULL
                    );
                    ''')
        print("books table script executed")  
          
        cur.execute("DROP TABLE IF EXISTS users_x_books")
        cur.execute('''
                    CREATE TABLE users_x_books(
                    userkey INTEGER NOT NULL,
                    bookkey INTEGER  NOT NULL,
                    FOREIGN KEY (userkey)
                    REFERENCES users (id) 
                    FOREIGN KEY (bookkey)
                    REFERENCES books (id) 
                    UNIQUE(userkey,bookkey )
                    );
                    ''')
        conn.commit()
        print("DB script executed")
    except:
        print(sys.exc_info()[0])
        conn.rollback()      
    finally:
        conn.close()

#This method will insert the user into database
def add_user(user):
    print("Inside add_user",user)
    inserted_user={}
    try:
        conn=connect_db()
        cur=conn.cursor()
        cur.execute("INSERT INTO users (userid, firstname, lastname, email, password) VALUES(?, ?, ?, ?, ?)", (user['userid'],user['firstname'], user['lastname'], user['email'], user['password']) )
        conn.commit()    
        inserted_user=get_users(user['userid'])             
    except:
        print(sys.exc_info()[0])
        conn.rollback()
    finally:
         conn.close()
    print("Exit from add_user", inserted_user)      
    return inserted_user     


#This method will insert the book into database
def add_book(book):
    print("Inside add_book",book)
    inserted_book={}
    try:
        conn=connect_db()
        cursr=conn.cursor()
        cursr.execute("INSERT INTO books(ISBN,title,author,publishdate)  VALUES (?,?,?,?)",(book['ISBN'],book['title'],book['author'],book['publishdate']))       
        conn.commit()
        inserted_book=get_books(book['ISBN'])      
    except:
        print(sys.exc_info()[0])
        conn.rollback()
    finally:
        conn.close()
    print("Exit from add_book",inserted_book)
    return inserted_book 
                   
#This method will insert the book into user wishlist database                   
def add_usr_whishlist(wishlist):
    print("inside add_usr_whishlist",wishlist)
    inserted_wishlist={}
    try:
        conn=connect_db()
        cursr=conn.cursor()
        user={}
        user=get_userkey(wishlist['userid'])
        book={}
        book=get_bookkey(wishlist['ISBN'])       
        cursr.execute("INSERT INTO users_x_books(userkey,bookkey) VALUES(?,?)", (user['userkey'], book['bookkey']))
        #cursr.execute("INSERT INTO users_x_books(userkey,bookkey) VALUES(select userkey from users where userid='testid1',select bookkey from books where ISBN='001')")  
        print("test")
        #cursr.execute("INSERT INTO users_x_books((select userkey from users where userid=?),(select bookkey from books where ISBN=?))", (wishlist['userid'],wishlist['ISBN']))
        conn.commit()
        inserted_wishlist= get_wishlist(wishlist['userid'],wishlist['ISBN'])       
    except:
        print(sys.exc_info()[0])
        conn.rollback()
    finally: 
        conn.close()
    print("Exit from add_usr_whishlist",inserted_wishlist)
    return inserted_wishlist

#This method will delete the book into user wishlist database     
def delete_usr_whislist(userid,ISBN):
    print("inside delete_usr_whislist",userid,ISBN)
    data={}
    try:
        conn=connect_db()
        cursr=conn.cursor()
        cursr.execute("DELETE FROM users_x_books WHERE userkey in (select userkey from users where userid=?) AND bookkey in (select bookkey from books where ISBN=?)", (userid,ISBN))
        conn.commit()
        data['status']="SUCCESS"
        data['message']="Deleted book ISBN "+ ISBN + " from userid "+userid +" wishlist"      
    except:
        print(sys.exc_info()[0])
        data['status']="FAILED"
        data['message']="unable to delete  book ISBN  "+ ISBN +" from userid "+ userid + " wishlist"
        conn.rollback()    
    finally: 
        conn.close()
    print("Exit from delete_usr_whislist",data)
    return data


#This method will fetch the user wishlist books for given userid 
def get_wishlist_by_userid(userid):
    print("inside get_wishlist_by_userid",userid)
    wishlists=[]
    try:
        conn=connect_db()
        conn.row_factory=sqlite3.Row
        cursr=conn.cursor()
        cursr.execute("SELECT usr.userid,bk.ISBN,bk.title,bk.author,bk.publishdate FROM  users_x_books uxb INNER JOIN users usr ON usr.userkey=uxb.userkey INNER JOIN books bk ON bk.bookkey=uxb.bookkey WHERE userid=? ", (userid,))      
        rows = cursr.fetchall()         
        for row in rows:           
            wishlist={}
            wishlist["userid"]=row["userid"] 
            wishlist["ISBN"]=row["ISBN"]     
            wishlist["title"]=row["title"]     
            wishlist["author"]=row["author"]              
            wishlist["publishdate"]=row["publishdate"]  
            wishlists.append(wishlist)       
    except:
        print(sys.exc_info()[0])
    print("Exit from get_wishlist_by_userid",userid)    
    return wishlists

#This method will fetch the user wishlist books for given userid and ISBN number
def get_wishlist(userid,ISBN):
    print("inside get_wishlist",userid,ISBN)
    wishlist={}
    try:
        conn=connect_db()
        conn.row_factory=sqlite3.Row
        cursr=conn.cursor()
        #cursr.execute("SELECT * FROM  users_x_books uxb JOIN users usr on(usr.id=uxb.userkey) JOIN books bk on (bk.id=uxb.bookkey) WHERE userid=? ANN ISBN=?", (userid,ISBN,))
        cursr.execute("SELECT usr.userid,bk.ISBN,bk.title,bk.author,bk.publishdate FROM  users_x_books oxb INNER JOIN books bk ON oxb.bookkey=bk.bookkey INNER JOIN users usr ON oxb.userkey=usr.userkey WHERE userid=? AND ISBN=?", (userid, ISBN))
        row=cursr.fetchone()            
        if (row != None): 
            wishlist["userid"]=row["userid"] 
            wishlist["ISBN"]=row["ISBN"]     
            wishlist["title"]=row["title"]     
            wishlist["author"]=row["author"]  
            wishlist["publishdate"]=row["publishdate"]                         
    except:
        print(sys.exc_info()[0])       
    return wishlist

#This method will fetch the user from given database for given userid
def get_users(userid):
    print("inside get user ",userid)
    user={}
    try:
        conn=connect_db()
        conn.row_factory=sqlite3.Row
        cursr=conn.cursor()
        cursr.execute("SELECT * FROM  users WHERE userid = ?", (userid,))
        row=cursr.fetchone()     
        if(row != None):           
            user["userid"]=row["userid"]
            user["firstname"]=row["firstname"]
            user["lastname"]=row["lastname"]
            user["email"]=row["email"]   
    except:
        print(sys.exc_info()[0])      
    return user

#This method will fetch the userkey from given database for given userid
def get_userkey(userid):
    print("inside get_userkey ",userid)
    user={}
    try:
        conn=connect_db()
        conn.row_factory=sqlite3.Row
        cursr=conn.cursor()
        cursr.execute("SELECT userkey FROM  users WHERE userid = ?", (userid,))
        row=cursr.fetchone()     
        if(row != None):           
            user["userkey"]=row["userkey"]            
    except:
        print(sys.exc_info()[0])     
    print("Exit from get_userkey ",userid) 
    return user    

#This method will delete the book into user wishlist database     
def delete_user(userid):
    print("inside delete_user",userid)
    data={}
    try:
        conn=connect_db()
        cursr=conn.cursor()
        cursr.execute("DELETE FROM users WHERE userid=?", (userid,))
        conn.commit()
        data['status']="SUCCESS"
        data['message']="Deleted user, userid "+ userid       
    except:
        print(sys.exc_info()[0])
        data['status']="FAILED"
        data['message']="unable  to delete user for userid "+ userid 
        conn.rollback()    
    finally: 
        conn.close()
    print("Exit from delete_user",data)
    return data

#This method will fetch the bookkey from database for given ISBN
def get_books(ISBN):
    print("inside get_books",ISBN)
    book={}
    try:
        conn=connect_db()
        conn.row_factory=sqlite3.Row
        cursr=conn.cursor()
        cursr.execute("SELECT * FROM  books WHERE ISBN=? ", (ISBN,))
        row=cursr.fetchone()
        if(row!=None):         
            book["ISBN"]=row["ISBN"]
            book["title"]=row["title"]
            book["author"]=row["author"]
            book["publishdate"]=row["publishdate"]      
    except:
        print(sys.exc_info()[0])     
    print("Exit from get_books",book)
    return book

#This method will fetch the books from database for given ISBN
def get_bookkey(ISBN):
    print("inside get_bookkey",ISBN)
    book={}
    try:
        conn=connect_db()
        conn.row_factory=sqlite3.Row
        cursr=conn.cursor()
        cursr.execute("SELECT bookkey FROM  books WHERE ISBN=? ", (ISBN,))
        row=cursr.fetchone()
        if(row!=None):         
            book["bookkey"]=row["bookkey"]              
    except:
        print(sys.exc_info()[0])     
    print("Exit from get_bookkey",book)
    return book


#This method will delete the book into user wishlist database     
def delete_book(ISBN):
    print("inside delete_book",ISBN)
    data={}
    try:
        conn=connect_db()
        cursr=conn.cursor()
        cursr.execute("DELETE FROM books where ISBN=?", (ISBN,))
        conn.commit()
        data['status']="SUCCESS"
        data['message']="Deleted book, ISBN "+ ISBN       
    except:
        print(sys.exc_info()[0])
        data['status']="FAILED"
        data['message']="Unable to delete  book for ISBN  "+ ISBN 
        conn.rollback()    
    finally: 
        conn.close()
    print("Exit from delete_book",data)
    return data
execute_script()

#This api will create the user 
@app.route('/api/users', methods=['POST'])
def api_add_user():
    user=request.get_json()
    print("user input",user)
    return jsonify(add_user(user))

#This api will fetch the user  by userid
@app.route('/api/users/<userid>', methods=['GET'])
def api_get_user(userid):
    user=request.get_json()
    print("user input",user)   
    return jsonify(get_users(userid))

#This api will delete the book from  user wishlist 
@app.route('/api/users/<userid>', methods=['DELETE'])
def api_delete_user(userid):
    return jsonify(delete_user(userid)) 

#This api will create the book 
@app.route('/api/books', methods=['POST'])
def api_add_books():
    book=request.get_json()
    return jsonify(add_book(book))

#This api will delete the book from  user wishlist 
@app.route('/api/books/<ISBN>', methods=['DELETE'])
def api_delete_book(ISBN):
    return jsonify(delete_book(ISBN)) 

#This api will fetch the book by userid
@app.route('/api/books/<ISBN>', methods=['GET'])
def api_get_books(ISBN):
    book=request.get_json()
    return jsonify(get_books(ISBN))

#This api will add the book into user wishlist
@app.route('/api/wishlist',methods=['POST'])
def api_add_wishlist():
    wishlist=request.get_json()
    return jsonify(add_usr_whishlist(wishlist))      

#This api will delete the book from  user wishlist 
@app.route('/api/wishlist/<userid>/<ISBN>', methods=['DELETE'])
def api_delete_wishlist(userid,ISBN):
    return jsonify(delete_usr_whislist(userid,ISBN)) 
 
#This api will fetch the user wish by userid
@app.route('/api/wishlist/<userid>',methods=['GET'])
def api_get_wishlist(userid):
    return jsonify(get_wishlist_by_userid(userid))

@app.route('/')
def index():
    String1='''Welcome to wishlist API's '''             
    return String1

app.run()