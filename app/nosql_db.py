#!/usr/bin/env python3
import sys


def get_collection(client):
    # creating database
    mydb = client["bozena"]
    # creating collection
    return mydb["test_user"]

def insert(collection, data):
    row = {"id": data[0],
             "first_name": data[1],
             "second_name": data[2],
             "email": data[3],
             "ui_lang": data[4],
             "ui_settings": data[5],
             "employee_account": data[6],
             "access_rights": data[7],
             "logon_status": data[8],
             "logon_last_modif": data[9]}

    result = collection.insert_one(row)

def delete(collection, query):
    x = collection.delete_many(query)

def drop_collection(collection):
    collection.drop()

def close(client):
    client.close()



