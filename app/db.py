# http://flask.pocoo.org/docs/1.0/tutorial/database/
import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g:
        conn = psycopg2.connect(
            host="localhost",
            database="narnia",
            user="admin",
            password="admin")
        # g.db.row_factory = sqlite3.Row


    return conn

def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()

def init_db():
    conn = get_db()
    "id,first_name,second_name,email,ui_lang,ui_settings,employee_account,access_rights,logon_status,logon_last_modif"
    cur = conn.cursor()
    comm = "INSERT INTO test_user(id,first_name,second_name,email,ui_lang,ui_settings,employee_account,access_rights,logon_status,logon_last_modif) VALUES (9,\'Vlad\',\'Ludor\', 'vlad.ludor@gmail.com', 'sk','test', FALSE, 'admin', 1,'2021-01-02');"
    cur.execute(comm)
    cur.close()
    conn.commit()

@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

