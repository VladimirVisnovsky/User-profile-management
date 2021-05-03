from flask_login import UserMixin

from db import get_connection

class User(UserMixin):
    def __init__(self, id_, first_name, second_name, email, ui_lang, ui_settings, employee_account, access_rights, logon_status, logon_last_modif):
        self.id = id_
        self.first_name = first_name
        self.second_name = second_name
        self.email = email
        self.ui_lang = ui_lang
        self.ui_settings = ui_settings
        self.employee_account = employee_account
        self.access_rights = access_rights
        self.logon_status = logon_status
        self.logon_last_modif = logon_last_modif

    @staticmethod
    def get(user_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM test_user WHERE id = %s", [user_id,]
        )
        user = cur.fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], first_name=user[1], second_name=user[2], email=user[3], ui_lang=user[4], ui_settings=user[5],
            employee_account=user[6], access_rights=user[7], logon_status=user[8], logon_last_modif=user[9]
        )
        return user

    @staticmethod
    def create(id_, first_name, second_name, email, ui_lang, ui_settings, employee_account, access_rights, logon_status, logon_last_modif):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO test_user (id, first_name, second_name, email, ui_lang, ui_settings, employee_account, access_rights, logon_status, logon_last_modif) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [id_, first_name, second_name, email, ui_lang, ui_settings, employee_account, access_rights, logon_status, logon_last_modif]
        )
        cur.close()
        conn.commit()

