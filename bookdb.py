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

