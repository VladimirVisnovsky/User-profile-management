#!/usr/bin/env python3
import timeit
import postgre_db
import os
import nosql_db
from pymongo import MongoClient
from create_table import create_tables
from gener.create_test_data import populate_table
import datetime

CLIENT = MongoClient("mongodb://localhost:27017")

def timeit_run_tests():

    tests = [("Select all test", "select_all_test"),
             ("Insert one row test", "insert_one_row_test"),
             ("Delete one row test", "delete_one_row_test"),
             ("Delete multiple rows test", "delete_multiple_rows_test"),
             ("Table drop test", "drop_table_test")]

    datasets = ['dataHundred.csv', 'data10Thousand.csv'] #, 'dataMillion.csv'


    for dataset in datasets:
        print('Creating test_user table and populating it with ' + dataset + '. This process might take several minutes.')
        create_tables()
        populate_table(dataset)
        print('Table created and populated. Running tests:')
        print()

        for test in tests:
            run_test(test[0], test[1])


def run_test(test_name, method_name):
    print(test_name)
    print("PostgreSQL:")
    elapsed_time = timeit.timeit(method_name + "_postgre()", "from __main__ import " + method_name + "_postgre", number=1)
    print("Time:", elapsed_time)
    print("NoSQL:")
    elapsed_time = timeit.timeit(method_name + "_nosql()", "from __main__ import " + method_name + "_nosql", number=1)
    print("Time:", elapsed_time)
    print()

def select_all_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_user")
    cur.close()
    conn.commit()

def select_all_test_nosql():
    pass

def insert_one_row_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    logon_last_modif = float(datetime.datetime.timestamp(datetime.datetime.now()))
    cur.execute(
        "INSERT INTO test_user (id, first_name, second_name, email, ui_lang, ui_settings, employee_account, access_rights, logon_status, logon_last_modif) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        [999999999, "Peter", "Parker", "peter.parker@gmail.com", "sk", "default ui settings", True, "complete access", 2, logon_last_modif]
    )
    cur.close()
    conn.commit()

def insert_one_row_test_nosql():
    pass

def delete_one_row_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM test_user WHERE id='1';")
    cur.close()
    conn.commit()

def delete_one_row_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"id": {"$regex": "1"}}
    nosql_db.delete(coll, query)

def delete_multiple_rows_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM test_user WHERE first_name LIKE '%o%';")
    cur.close()
    conn.commit()

def delete_multiple_rows_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"first_name": {"$regex": "[a-zA-Z]*o[a-zA-Z]*"}}
    nosql_db.delete(coll, query)

def drop_table_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE test_user;")
    cur.close()
    conn.commit()

def drop_table_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    nosql_db.drop_collection(coll)


timeit_run_tests()