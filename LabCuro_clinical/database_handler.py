import sqlite3


def create(creation_command, db_name):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(creation_command)
    db.commit()
    db.close()
    
def insert_data(varss, dicts, db_name):
    #print 'im in isert data'
    db = sqlite3.connect(db_name)
    #print 'i connected'
    cursor = db.cursor()
    cursor.execute(varss, dicts)
    #print 'exceuted'
    db.commit()
    #print 'commited'
    db.close()
    #print 'closed'
    
def query_data(db_name, query):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    t = cursor.execute(query)
    query_list = [x[0] for x in t]
    db.close()
    return query_list
    #cursor.execute('''SELECT name, email, phone FROM tablename''')
    #all_rows = cursor.fetchall()
    #list_labservice = []
    #for row in all_rows:
     #   temp_str = ('{0} : {1}, {2}'.format(row[0], row[1], row[2]))   
      #  list_labservice.append(temp_str)
    #db.close()
    #return list_labservice






