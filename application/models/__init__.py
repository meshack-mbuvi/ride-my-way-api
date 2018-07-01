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
        try:
            cursor.execute('SELECT 1 from {}' . format('rides'))
        except Exception as e:
            command = 'CREATE TABLE rides (ride_id serial PRIMARY KEY, \
            owner_id serial, \
            start_point varchar(255), \
            destination varchar(255), \
            start_time varchar(50) NOT NULL, \
            route varchar(255) NOT NULL, \
            available_space Int NOT NULL, \
            FOREIGN KEY (owner_id) REFERENCES users(user_id) )'
            cursor.execute(command)
            try:
                cursor.execute('SELECT 1 from {}' . format('requests'))
            except Exception as e:
                command = 'CREATE TABLE requests (req_id serial PRIMARY KEY,\
                       date_created timestamp,\
                       ride_id serial,\
                       user_id serial,\
                       status boolean default null, \
                       FOREIGN KEY (ride_id) REFERENCES rides(ride_id), \
                       FOREIGN KEY (user_id) REFERENCES users(user_id) )'
                cursor.execute(command)
    return
