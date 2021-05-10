#!/usr/bin/env python3
import csv
import os
import random
import datetime
import sys

import psycopg2

def read_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    return ["{}".format(line.strip()) for line in lines]


def generate_data():
    names = read_file(f'{os.path.dirname(os.path.realpath(__file__))}/names.txt')
    last_names = read_file(f'{os.path.dirname(os.path.realpath(__file__))}/last_names.txt')
    languages = read_file(f'{os.path.dirname(os.path.realpath(__file__))}/languages.txt')


    with open (f'{os.path.dirname(os.path.realpath(__file__))}/data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID", "first name", "second name", "email", "ui_lang", "ui_settings", "employee_account", "access_rights","logon_status","logon_last_modif"])
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for i in range(10000):
            name = random.choice(names)
            last_name = random.choice(last_names)
            email = name.lower() + "." + last_name.lower() + str(random.randint(0,1000)) + "@gmail.com"
            lang = random.choice(languages)
            writer.writerow([i, name, last_name, email, lang, "default", random.choice([True, False]), "complete access", 2, date])


def populate_table():
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

        with open(f'{os.path.dirname(os.path.realpath(__file__))}/data.csv', 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            next(csv_reader)
            for row in csv_reader:
                # row variable is a list that represents a row in csv
                # insert into table
                cur.execute(
                    "INSERT INTO test_user (id, first_name, second_name, email, ui_lang, ui_settings, employee_account, access_rights, logon_status, logon_last_modif) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]]
                )
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

generate_data()
