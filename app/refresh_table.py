#!/usr/bin/env python3
import user
import db
import datetime

def refresh():
    conn = db.get_connection()
    cur = conn.cursor()
    current_time = datetime.datetime.timestamp(datetime.datetime.now())

    cur.execute("UPDATE test_user AS tu SET logon_status = 0 WHERE tu.logon_last_modif::float < %s - 60 ", [current_time])

    cur.close()
    conn.commit()


