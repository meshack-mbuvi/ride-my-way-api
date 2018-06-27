from psycopg2 import connect

dbname = 'ridemyway'
user = 'ridemyway'
host = 'localhost'
password = 'ridemyway'


class db():

    def connect(self, dbname):
        dbname = dbname
        con = connect(database=dbname, user=user, host=host, password=password)
        con.autocommit = True
        return con

    def create_all(self, dbname=dbname):
        # Create all tables here
        con = self.connect(dbname)
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
                       destination varchar(255), \
                       start_time varchar(50) NOT NULL, \
                       route varchar(255) NOT NULL, \
                       available_space Int NOT NULL, \
                       FOREIGN KEY (owner_id) REFERENCES users(user_id) )'
        )

        try:
            cur = con.cursor()
            # create table one by one
            print("Creating relations")
            for command in commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            con.commit()
            print("Done.")
        except (Exception) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

    def drop_all(self, dbname=dbname):
        con = self.connect(dbname)
        commands = (
            'DROP TABLE "users" CASCADE',
            'DROP TABLE "rides" CASCADE')
        try:
            con.autocommit = True
            cur = con.cursor()
            # create table one by one
            print("Deleting relations")
            for command in commands:
                cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            con.commit()
            print("Done.")
        except (Exception) as error:
            print(error)
        finally:
            if con is not None:
                con.close()

if __name__ == '__main__':
    db = db()
    db.create_all()
