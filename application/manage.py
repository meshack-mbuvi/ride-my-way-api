from psycopg2 import connect

dbname = 'ridemyway'
user = 'ridemyway'
host = 'localhost'
password = 'ridemyway'


class database():

    def connect(self):
        connection = connect(database=dbname, user=user, host=host, password=password)
        connection.autocommit = True
        return connection

    def create_all(self):
        # Create all tables here
        connection = self.connect()
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
                       startPoint varchar(255), \
                       destination varchar(255), \
                       startTime varchar(50) NOT NULL, \
                       route varchar(255) NOT NULL, \
                       availablePpace Int NOT NULL, \
                       FOREIGN KEY (owner_id) REFERENCES users(user_id) )'
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

    def drop_all(self):
        connection = self.connect()
        commands = (
            'DROP TABLE "users" CASCADE',
            'DROP TABLE "rides" CASCADE')
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
