import os
from psycopg2 import connect

class Database(object):

    def __init__(self):
        self.dbname = os.getenv("DATABASE_NAME")
        self.user = os.getenv("USER")
        self.password = os.getenv("PASSWORD")
        self.host = os.getenv("HOST")
        print("...connecting")
        connection = connect(database=self.dbname,
                             user=self.user, host=self.host, password=self.password)
        connection.autocommit = True
        self.connection = connection

    def create_all(self):
        print("... starting creation of relations")
        commands = (
            'CREATE TABLE IF NOT EXISTS users (user_id serial PRIMARY KEY, \
                        username varchar(255), \
                        email varchar(50) NOT NULL, \
                        password varchar(255) NOT NULL, \
                        phone varchar(255) NOT NULL, driver boolean )',

            'CREATE TABLE IF NOT EXISTS rides (ride_id serial PRIMARY KEY, \
                       owner_id serial, \
                       start_point varchar(255), \
                       destination varchar(255), \
                       start_time timestamp NOT NULL, \
                       route varchar(255) NOT NULL, \
                       available_space Int NOT NULL, \
                       FOREIGN KEY (owner_id) REFERENCES users(user_id) )',
            'CREATE TABLE IF NOT EXISTS requests (req_id serial PRIMARY KEY,\
                       date_created timestamp,\
                       ride_id serial,\
                       user_id serial,\
                       status boolean, \
                       FOREIGN KEY (ride_id) REFERENCES rides(ride_id), \
                       FOREIGN KEY (user_id) REFERENCES users(user_id) )'
        )

        try:
            cursor = self.connection.cursor()
            # create table one by one
            print("Creating relations")
            for command in commands:
                cursor.execute(command)
            # close communication with the PostgreSQL database server
            cursor.close()
            print("Done.")
        except (Exception) as error:
            print(error)

    def drop_all(self):
        commands = (
            'DROP TABLE "users" CASCADE',
            'DROP TABLE "rides" CASCADE',
            'DROP TABLE "requests" CASCADE')
        try:
            cursor = self.connection.cursor()
            # drop table one by one
            print("Deleting relations")
            for command in commands:
                cursor.execute(command)
            # close communication with the PostgreSQL database server
            cursor.close()
            print("Done.")
        except (Exception) as error:
            print(error)

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor


if __name__ == '__main__':
    dbObject = Database()
    dbObject.create_all()
