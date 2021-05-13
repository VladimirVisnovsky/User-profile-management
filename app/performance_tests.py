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
ACTUAL_TIME = float(datetime.datetime.timestamp(datetime.datetime.now()))

def timeit_run_tests():

    tests = [("TEST: select one row", "select_one_row_test"),
             ("TEST: select active users", "select_active_users_test"),
             ("TEST: select all", "select_all_test"),
             ("TEST: insert one row", "insert_one_row_test"),
             ("TEST: update one row", "update_one_row_test"),
             ("TEST: update active users", "update_active_users_test"),
             ("TEST: delete one row", "delete_one_row_test"),
             ("TEST: delete inactive users", "delete_inactive_users_test"),
             ("TEST: drop table", "drop_table_test")]

    datasets = ['dataHundred.csv', 'data10Thousand.csv'] # , 'dataMillion.csv'


    for dataset in datasets:
        print('Creating test_user table and populating it with ' + dataset + '. This process might take several minutes.')
        create_tables()
        populate_table(dataset)

        if (dataset == 'dataHundred.csv'):
            print('Table created and populated. 54 active users out of total 100.')
        elif (dataset == 'data10Thousand.csv'):
            print('Table created and populated. 4993 active users out of total 10 000.')
        elif (dataset == 'dataMillion.csv'):
            print('Table created and populated. 498 995 active users out of total 1 000 000.')
            
        print('Running tests:')
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

def select_one_row_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_user WHERE id='1'")
    cur.close()
    conn.commit()

def select_one_row_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"id": {"$regex": "1"}}
    nosql_db.select(coll, query)

def select_active_users_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_user WHERE logon_status='2'")
    cur.close()
    conn.commit()

def select_active_users_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"logon_status": {"$regex": "2"}}
    nosql_db.select(coll, query)

def select_all_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_user")
    cur.close()
    conn.commit()

def select_all_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    nosql_db.select_all(coll)

def insert_one_row_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO test_user (id, first_name, second_name, email, ui_lang, ui_settings, employee_account, access_rights, logon_status, logon_last_modif)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        [999999999, "Peter", "Parker", "peter.parker@gmail.com", "sk", "default ui settings", True, "complete access", 2, ACTUAL_TIME]
    )
    cur.close()
    conn.commit()

def insert_one_row_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    data = ["999999999", "Peter", "Parker", "peter.parker@gmail.com", "sk", "default ui settings", "True", "complete access", "2", str(ACTUAL_TIME)]
    nosql_db.insert(coll, data)

def update_one_row_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE test_user SET logon_last_modif=%s WHERE id='1';", [ACTUAL_TIME])
    cur.close()
    conn.commit()

def update_one_row_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"id": {"$regex": "1"}}
    data = {"$set": {"logon_last_modif": ACTUAL_TIME}}
    nosql_db.update(coll, query, data)

def update_active_users_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE test_user SET logon_last_modif=%s WHERE logon_status='2';", [ACTUAL_TIME])
    cur.close()
    conn.commit()

def update_active_users_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"logon_status": {"$regex": "2"}}
    data = {"$set": {"logon_last_modif": ACTUAL_TIME}}
    nosql_db.update_many(coll, query, data)

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

def delete_inactive_users_test_postgre():
    conn = postgre_db.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM test_user WHERE logon_status='0';")
    cur.close()
    conn.commit()

def delete_inactive_users_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"logon_status": {"$regex": "0"}}
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

