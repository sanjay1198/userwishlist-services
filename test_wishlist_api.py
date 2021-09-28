import json

#This testcase will add the user into database
def test_success_adduser(app,client):
    data={'userid':'testid1','firstname':'Jhon','lastname':'test1lname','email':'test1@test.com','password':'asd'}
    res=client.post('/api/users',data=json.dumps(data),headers={'Content-Type': 'application/json'})
    expected={'userid':'testid1','firstname':'Jhon','lastname':'test1lname','email':'test1@test.com'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will fail to the user into database
def test_uniqueconstraint_failed_adduser_(app,client):
    data={'userid':'testid1','firstname':'Jhon','lastname':'test1lname','email':'test1@test.com','password':'asd'}
    res=client.post('/api/users',data=json.dumps(data),headers={'Content-Type': 'application/json'})
    expected={}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))
    
#This testcase will add to the book into database
def test_success_addbooks(app,client):
    data={'ISBN':'001','author':'Robbert','publishdate':'test1lname','title':'Python coding'}
    res=client.post('/api/books',data=json.dumps(data),headers={'Content-Type': 'application/json'})
    expected={'ISBN':'001','author':'Robbert','publishdate':'test1lname','title':'Python coding'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will fail to add the book into database
def test_uniqueconstraint_failed_addbooks(app,client):
    data={'ISBN':'001','author':'Robbert','publishdate':'test1lname','title':'Python coding'}
    res=client.post('/api/books',data=json.dumps(data),headers={'Content-Type': 'application/json'})
    expected={}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will successfully fetch the added user from into database    
def test_success_fetchuser(app,client):
    res=client.get('/api/users/testid1')
    expected={'userid':'testid1','firstname':'Jhon','lastname':'test1lname','email':'test1@test.com'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))
    
#This testcase will successfully fetch the added book from into database 
def test_success_fetchbook(app,client):
    res=client.get('/api/books/001')
    expected={'ISBN':'001','author':'Robbert','publishdate':'test1lname','title':'Python coding'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will successfully add the the book to user wishlist 
def test_sucess_addbook_userwishlist(app,client):
    data={'userid':'testid1','ISBN':'001'}
    res=client.post('/api/wishlist',data=json.dumps(data),headers={'Content-Type': 'application/json'})
    expected={'userid':'testid1','ISBN':'001','author':'Robbert','publishdate':'test1lname','title':'Python coding'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will fail to add the the book to user wishlist due to unique constraint
def test_uniqueconstraint_addbook_userwishlist(app,client):
    data={'userid':'testid1','ISBN':'001'}
    res=client.post('/api/wishlist',data=json.dumps(data),headers={'Content-Type': 'application/json'})
    expected={}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will fail to add the the book to user wishlist due to data issue
def test_failed_addbook_userwishlist(app,client):
    data={'userid':'testid1','ISBN':'002'}
    res=client.post('/api/wishlist',data=json.dumps(data),headers={'Content-Type': 'application/json'})
    expected={}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))
    
#This testcase will succefully fetch the userwishlist for given user
def test_success_fetchuserwishlist(app,client):
    res=client.get('/api/wishlist/testid1')
    expected=[{'ISBN':'001','author':'Robbert','publishdate':'test1lname','title':'Python coding','userid':'testid1'}]
    print(expected)
    #print(json.loads(res.get_data(as_text=True))
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))
    
#This testcase will succefully delete  the book from user wishlist
def test_success_deleteuserwishlist(app,client):
    res=client.delete('/api/wishlist/testid1/001')
    expected={'status':'SUCCESS','message':'Deleted book ISBN 001 from userid testid1 wishlist'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will failed to fetch the data for user wishlist
def test_failed_fetchuserwishlist(app,client):
    res=client.get('/api/wishlist/testid1')
    expected=[]
    print(expected)
    #print(json.loads(res.get_data(as_text=True))
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will delete the user from data base      
def test_success_deleteuser(app,client):
    res=client.delete('/api/users/testid1')
    expected={'status':'SUCCESS','message':'Deleted user, userid testid1'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will delete the book from data base 
def test_success_deletebooks(app,client):
    res=client.delete('/api/books/001')
    expected={'status':'SUCCESS','message':'Deleted book, ISBN 001'}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will failed to get the record or will fetch empty user record from data base 
def test_failed_fetchuser(app,client):
    res=client.get('/api/users/testid1')
    expected={}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

#This testcase will failed to the record or will fetch empty book record from data base 
def test_failed_fetchbook(app,client):
    res=client.get('/api/books/001')
    expected={}
    assert res.status_code==200
    assert expected==json.loads(res.get_data(as_text=True))

    
