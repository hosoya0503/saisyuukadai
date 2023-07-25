import os,psycopg2

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    return connection

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT title, author, publisher, isbn FROM books_management'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return rows

def insert_book(title, author, publisher, isbn):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'INSERT INTO books_management VALUES(default, %s, %s, %s, %s)'
    
    cursor.execute(sql, (title, author, publisher, isbn))
    
    connection.commit()
    cursor.close()
    connection.close()

def delete_book(isbn):
    sql = "DELETE FROM books_management WHERE isbn=%s"
    count=0
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql, (isbn,))
        connection.commit()
    except psycopg2.DatabaseError:
        count = 1
    finally :
        connection.close()
        cursor.close()
    if count ==  1:
        return 0
    else :
        return