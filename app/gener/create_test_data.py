#!/usr/bin/env python3
import csv
import random
import datetime

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

names = read_file('names.txt')
last_names = read_file('last_names.txt')
languages = read_file('languages.txt')


with open ('data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["ID", "first name", "second name", "email", "ui_lang", "ui_settings", "employee_account", "access_rights","logon_status","logon_last_modif"])

    for i in range(10001):
        name = random.choice(names)
        last_name = random.choice(last_names)
        email = name.lower() + "." + last_name.lower() + "@gmail.com"
        lang = random.choice(languages)
        random_date = get_random_date(2020)
        writer.writerow([i, name, last_name, email, lang, "default", random.choice([True, False]), "complete access", 2, random_date])
