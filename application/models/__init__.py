from psycopg2 import connect

from application.manage import dbname

host = 'ec2-54-225-230-142.compute-1.amazonaws.com'
user = 'fykazngytmidee'
password = '7a940a85b94644e69d871928b9dc8a7b1dda264fcfb4724ca6c0f423514b230b'
database = 'du15ldvvdve7g'
connection = connect(database=database, user=user, host=host, password=password)
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
            start_time timestamp NOT NULL, \
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
