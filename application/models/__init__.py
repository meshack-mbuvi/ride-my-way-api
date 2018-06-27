from psycopg2 import connect

from application.manage import dbname

# dbname = 'ridemyway'
user = 'ridemyway'
host = 'localhost'
password = 'ridemyway'

con = connect(database=dbname, user=user, host=host, password=password)
con.autocommit = True
cur = con.cursor()


# create user table
def create_all():
    cur = con.cursor()
    try:
        cur.execute('SELECT 1 from {}' . format('users'))
    except Exception as e:
        command = 'CREATE TABLE users (user_id serial PRIMARY KEY, \
        username varchar(255), \
        email varchar(50) NOT NULL, \
        password varchar(255) NOT NULL, \
        phone varchar(255) NOT NULL, driver boolean )'
        cur.execute(command)
