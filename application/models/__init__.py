from psycopg2 import connect

from application.manage import dbname

# dbname = 'ridemyway'
user = 'ridemyway'
host = 'localhost'
password = 'ridemyway'

connection = connect(database=dbname, user=user, host=host, password=password)
connection.autocommit = True
cursor = connection.cursor()


# create user table
def create_all():
    cursor = connection.cursor()
    try:
        cursor.execute('SELECT 1 from {}' . format('users'))
    except Exception as e:
        command = 'CREATE TABLE users (user_id serial PRIMARY KEY, \
        username varchar(255), \
        email varchar(50) NOT NULL, \
        password varchar(255) NOT NULL, \
        phone varchar(255) NOT NULL, driver boolean )'
        cursor.execute(command)
