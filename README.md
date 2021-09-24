# userwishlist-services 
 This application supports the APIs to manage the user, book and user wishlist. 
 Application provides API's to create, fetch and delete the user and books record. Here user and books will be treated as parent data. 
 userid and ISBN number considered as natural number for user and book respectively.
 
 Application provides APIs to manage the userwishlsit. User can add the books to wishlist by passing ISBN number and user id. 
 User can fetch all the books present in wishlist for given userid and delete the book from wishlist. Based on UI funcationality we can utilize the API accordingly.

This application provides below APIs 
1. Add user  :
   This API will add the  incoming user in to the system. API will respond with user data if insertion is successfull otherwise API will return empty object 
      
      API             : http://<host>:<port>/api/users
      Request method  : POST
 
      Request         :
                        {
                           "userid"  : "Jhon001",
                           "firstname" : "Jhon",
                           "lastname" : "Smith",
                           "email"  : "jonsmith@test.com",
                           "password"  : "hdfkfk"
                       }
  
3. Add book 
   This API will add the incoming books in to the system. API will respond with books data if insertion is successfull otherwise API will return empty object.
      API             : http://<host>:<port>/api/books
      Request method  : POST
 
      Request         :
                          {
                             "ISBN"  : "978-1-57819-909-4",
                             "author" : "Robert",
                             "publishdate" : "20 Dec 2020",
                             "title"  : "Python coding"
                         }
  
5. Add book to wishlist 
   This API will add the books in to the system. API will resposnd with added books data along with userid if insertion is successfull for wishlist otherwise 
    API will return   empty object. 
    
      API             : http://<host>:<port>/api/wishlist
      Request method  : POST
      Request         :
                        {
                            "userid":"Jhon001",
                            "ISBN":"978-1-57819-909-4"
                        }
6. Get user by userid 
   This API will fecth the user record for given userid. API will respond with user data if fetch is successfull otherwise API will return empty object.
      
       API             : http://<host>:<port>/api/users/<userid>
       Request method  : GET
   
7. Get book by ISBN  
   This API will fecth the books record for given ISBN. API will respond with books data if fetch is successfull otherwise API will return empty object.
       API             : http://<host>:<port>/api/books/<ISBN>
       Request method  : GET
  
8. Get userwishlist by userid.
   This API will fecth the user record for given userid. API will respond with user data if fetch is successfull otherwise API will return empty object.
       
       API             : http://<host>:<port>/api/wishlist/<userid>
       Request method  : GET
  
9. Delete book from user wishlist.
   API will return success message if deletetion is successfull otherwise API will return failure message.
       
       API             : http://<host>:<port>/api/wishlist/<userid>/<ISBN>
       Request method  : DELETE
  
10. Delete user by user id . 
    API will return success message if deletetion is successfull otherwise API will return failure message.
       
       API             : http://<host>:<port>/api/users/<userid>
       Request method  : DELETE
  
11. Delete the book by ISBN.
    API will return success message if deletetion is successfull otherwise API will return failure message.
      
       API             : http://<host>:<port>/api/books/<ISBN>
       Request method  : DELETE
