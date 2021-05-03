# http://flask.pocoo.org/docs/1.0/tutorial/database/
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_connection():
    conn = None
    if "db" not in g:
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
    conn = get_db()
    # cur = conn.cursor() 117909486482005620137
    # comm = "INSERT INTO test_user(id,first_name,second_name,email,ui_lang,ui_settings,employee_account,access_rights,logon_status,logon_last_modif) VALUES (9,\'Vlad\',\'Ludor\', 'vlad.ludor@gmail.com', 'sk','test', FALSE, 'admin', 1,'2021-01-02');"
    # cur.execute(comm)
    # cur.close()
    # conn.commit()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    conn = get_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

