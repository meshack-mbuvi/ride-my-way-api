from psycopg2 import connect

dbname = 'ridemyway'
user = 'ridemyway'
host = 'localhost'
password = 'ridemyway'


class database():

    def connect(self, dbname):
        dbname = dbname
        connection = connect(database=dbname,
                             user=user, host=host, password=password)
        connection.autocommit = True
        return connection

    def create_all(self, dbname=dbname):
        # Create all tables here
        connection = self.connect(dbname)
        commands = (
            'DROP TABLE "users" CASCADE',
            'CREATE TABLE users (user_id serial PRIMARY KEY, \
                        username varchar(255), \
                        email varchar(50) NOT NULL, \
                        password varchar(255) NOT NULL, \
                        phone varchar(255) NOT NULL, driver boolean )',

            'DROP TABLE "rides" CASCADE',
            'CREATE TABLE rides (ride_id serial PRIMARY KEY, \
                       owner_id serial, \
                       start_point varchar(255), \
                       destination varchar(255), \
                       start_time varchar(50) NOT NULL, \
                       route varchar(255) NOT NULL, \
                       available_space Int NOT NULL, \
                       FOREIGN KEY (owner_id) REFERENCES users(user_id) )',
            'DROP TABLE "requests" CASCADE',
            'CREATE TABLE requests (req_id serial PRIMARY KEY,\
                       date_created timestamp,\
                       owner_id serial,\
                       user_id serial,\
                       status boolean, \
                       FOREIGN KEY (owner_id) REFERENCES users(user_id), \
                       FOREIGN KEY (user_id) REFERENCES users(user_id) )'
        )

        try:
            cursor = connection.cursor()
            # create table one by one
            print("Creating relations")
            for command in commands:
                cursor.execute(command)
            # close communication with the PostgreSQL database server
            cursor.close()
            # commit the changes
            connection.commit()
            print("Done.")
        except (Exception) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

    def drop_all(self, dbname=dbname):
        connection = self.connect(dbname)
        commands = (
            'DROP TABLE "users" CASCADE',
            'DROP TABLE "rides" CASCADE',
            'DROP TABLE "requests" CASCADE')
        try:
            connection.autocommit = True
            cursor = connection.cursor()
            # create table one by one
            print("Deleting relations")
            for command in commands:
                cursor.execute(command)
            # close communication with the PostgreSQL database server
            cursor.close()
            # commit the changes
            connection.commit()
            print("Done.")
        except (Exception) as error:
            print(error)
        finally:
            if connection is not None:
                connection.close()

if __name__ == '__main__':
    dbObject = database()
    dbObject.create_all()
