#!/usr/bin/env python3
import timeit
import db
import os
import nosql_db
from pymongo import MongoClient

CLIENT = MongoClient("mongodb://localhost:27017")

def timeit_run_tests():

    print(timeit.timeit('select_all_test_postgre()', 'from __main__ import select_all_test_postgre', number=1))
    print(timeit.timeit('select_all_test_nosql()', 'from __main__ import select_all_test_nosql', number=1))

def delete_multiple_rows_test_nosql():
    coll = nosql_db.get_collection(CLIENT)
    query = {"first_name": {"$regex": "[a-zA-Z]*u[a-zA-Z]*"}}
    nosql_db.delete(coll, query)



def delete_multiple_rows_test_postgre():
    conn = db.get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM test_user WHERE first_name LIKE '%o%';")
    cur.close()
    conn.commit()


timeit_run_tests()
# select_all_test_postgre()
# select_all_test_nosql()
