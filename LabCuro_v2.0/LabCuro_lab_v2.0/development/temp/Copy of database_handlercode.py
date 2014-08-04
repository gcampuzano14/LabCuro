import sqlite3

db = sqlite3.connect('mydb')

def create(creation_command):
    cursor = db.cursor()
    cursor.execute(creation_command)
    db.commit()

def drop():
    cursor = db.cursor()
    cursor.execute('''DROP TABLE users''')
    db.commit()

def insert_data():
    cursor = db.cursor()
    name1 = 'Andres'
    phone1 = '3366858'
    email1 = 'user@example.com'
    # A very secure password
    password1 = '12345'
     
    name2 = 'John'
    phone2 = '5557241'
    email2 = 'johndoe@example.com'
    password2 = 'abcdef'
     
    # Insert user 1
    cursor.execute('''INSERT INTO users(name, phone, email, password)
                      VALUES(?,?,?,?)''', (name1,phone1, email1, password1))
    print('First user inserted')
    
    OR
    cursor.execute('''INSERT INTO users(name, phone, email, password)
                  VALUES(:name,:phone, :email, :password)''',
                  {'name':name1, 'phone':phone1, 'email':email1, 'password':password1})
     
    # Insert user 2
    cursor.execute('''INSERT INTO users(name, phone, email, password)
                      VALUES(?,?,?,?)''', (name2,phone2, email2, password2))
    print('Second user inserted')
    
    
    OR
    
    users = [(name1,phone1, email1, password1),
         (name2,phone2, email2, password2),
         (name3,phone3, email3, password3)]
    cursor.executemany(''' INSERT INTO users(name, phone, email, password) VALUES(?,?,?,?)''', users)

     
    db.commit()

#If you need to get the id of the row you just inserted use lastrowid:
def last_id():
    id = cursor.lastrowid
    print('Last row id: %d' % id)


def retrieve():
    cursor.execute('''SELECT name, email, phone FROM users''')
    user1 = cursor.fetchone() #retrieve the first row
    print(user1[0]) #Print the first column retrieved(user's name)
    all_rows = cursor.fetchall()
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))   
    
    The cursor object works as an iterator, invoking fetchall() automatically:
    cursor.execute('''SELECT name, email, phone FROM users''')
    for row in cursor:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))
    
    To retrive data with conditions, use again the "?" placeholder:
    user_id = 3
    cursor.execute('''SELECT name, email, phone FROM users WHERE id=?''', (user_id,))
    user = cursor.fetchone()
  
def     Updating (UPDATE) and Deleting (DELETE) Data():
    
    
    The procedure to update or delete data is the same as inserting data:
        
    # Update user with id 1
    newphone = '3113093164'
    userid = 1
    cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
    (newphone, userid))
     
    # Delete user with id 2
    delete_userid = 2
    cursor.execute('''DELETE FROM users WHERE id = ? ''', (delete_userid,))
     
    db.commit()  

def    Using SQLite Transactions():
    Transactions are an useful property of database systems. It ensures the atomicity of the Database. Use commit to save the changes:  
    cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
    (newphone, userid))
    db.commit() #Commit the change
    Or rollback to roll back any change to the database since the last call to commit: 
    cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
    (newphone, userid))
    # The user's phone is not updated
    db.rollback()

    We can use the Connection object as context manager to automatically commit or rollback transactions:
    
    name1 = 'Andres'
    phone1 = '3366858'
    email1 = 'user@example.com'
    # A very secure password
    password1 = '12345'
     
    try:
        with db:
            db.execute('''INSERT INTO users(name, phone, email, password)
                      VALUES(?,?,?,?)''', (name1,phone1, email1, password1))
    except sqlite3.IntegrityError:
        print('Record already exists')
    finally:
        db.close()
    
     SQLite Row Factory and Data Types
    
    The following table shows the relation between SQLite datatypes and Python datatypes:
    
        None type is converted to NULL
        int type is converted to INTEGER
        float type is converted to REAL
        str type is converted to TEXT
        bytes type is converted to BLOB
    
    The row factory class sqlite3.Row is used to access the columns of a query by name instead of by index:  
    db = sqlite3.connect('data/mydb')
    db.row_factory = sqlite3.Row
    cursor = db.cursor()
    cursor.execute('''SELECT name, email, phone FROM users''')
    for row in cursor:
        # row['name'] returns the name column in the query, row['email'] returns email column.
        print('{0} : {1}, {2}'.format(row['name'], row['email'], row['phone']))
    db.close()

     
#drop()
#create()

db.close()
