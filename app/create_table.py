#!/usr/bin/python3

import psycopg2
# from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    command = "CREATE TABLE test_user (id VARCHAR(255) PRIMARY KEY,first_name VARCHAR(255) NOT NULL,second_name VARCHAR(255) NOT NULL,email VARCHAR(255) UNIQUE NOT NULL,ui_lang VARCHAR(255) NOT NULL,ui_settings VARCHAR(255) NOT NULL,employee_account BOOLEAN NOT NULL,access_rights VARCHAR(255) NOT NULL,logon_status INTEGER NOT NULL,logon_last_modif VARCHAR(255) NOT NULL)"
    conn = None
    try:
        # read the connection parameters
        # params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(
                        host="localhost",
                        database="narnia",
                        user="admin",
                        password="admin")
        cur = conn.cursor()
        # create table
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
