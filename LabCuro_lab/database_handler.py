import sqlite3

def create(creation_command, db_name):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(creation_command)
    db.commit()
    db.close()
    
def insert_data(varss, dicts, db_name):
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    cursor.execute(varss, dicts)
    db.commit()
    db.close()
    
def query_data(db_name, query):
    print db_name
    db = sqlite3.connect(db_name)
    cursor = db.cursor()
    query_list = cursor.execute(query)
    return query_list




