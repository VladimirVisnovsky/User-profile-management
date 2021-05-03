#!/usr/bin/env python3
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext

TABLE_NAME = 'test_user'


def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="narnia",
        user="admin",
        password="admin")
    return conn


def close_db():
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", (TABLE_NAME,))
    return cur.fetchone()[0]
    
