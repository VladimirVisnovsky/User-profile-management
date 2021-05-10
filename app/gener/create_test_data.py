#!/usr/bin/env python3
import csv
import os
import random
import datetime
import sys

import psycopg2

# create function accepting a single parameter, the year as a four digit number
def get_random_date(year):
    # try to get a date
    try:
        return datetime.datetime.strptime('{} {}'.format(random.randint(1, 366), year), '%j %Y').date()
    # if the value happens to be in the leap year range, try again
    except ValueError:
        return get_random_date(year)

def read_file(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    return ["{}".format(line.strip()) for line in lines]

print()

def generate_data():
    names = read_file('gener/names.txt')
    last_names = read_file('gener/last_names.txt')
    languages = read_file('gener/languages.txt')


    with open ('gener/data.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["ID", "first name", "second name", "email", "ui_lang", "ui_settings", "employee_account", "access_rights","logon_status","logon_last_modif"])

        for i in range(100):
            name = random.choice(names)
            last_name = random.choice(last_names)
            email = name.lower() + "." + last_name.lower() + str(random.randint(0,1000)) + "@gmail.com"
            lang = random.choice(languages)
            random_date = get_random_date(2020)
            writer.writerow([i, name, last_name, email, lang, "default", random.choice([True, False]), "complete access", 2, random_date])


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

        with open('gener/data.csv', 'r') as read_obj:
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
