#!/usr/bin/env python3
import timeit
import db
import os
import nosql_db
from pymongo import MongoClient

CLIENT = MongoClient("mongodb://localhost:27017")

def timeit_run_tests():

    tests = [("Delete one row test", "delete_one_row_test"),
             ("Delete multiple rows test", "delete_multiple_rows_test"),
             ("Table drop test", "drop_table_test")]

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


def delete_one_row_test_postgre():
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM test_user WHERE id='1';")
    cur.close()
    conn.commit()

def delete_one_row_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"id": {"$regex": "1"}}
    nosql_db.delete(coll, query)

def delete_multiple_rows_test_postgre():
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM test_user WHERE first_name LIKE '%o%';")
    cur.close()
    conn.commit()

def delete_multiple_rows_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"first_name": {"$regex": "[a-zA-Z]*u[a-zA-Z]*"}}
    nosql_db.delete(coll, query)

def drop_table_test_postgre():
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE test_user;")
    cur.close()
    conn.commit()

def drop_table_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    nosql_db.drop_collection(coll)



timeit_run_tests()
# select_all_test_postgre()
# select_all_test_nosql()
