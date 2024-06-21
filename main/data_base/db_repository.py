import sqlite3
import uuid
from sqlite3 import Error
from dotenv import load_dotenv
import os

from main.const.database_const import TABLE_USERS
from main.data_base.database_sql_statements import insert_user_sql, create_users_table, create_roles_table, \
    create_users_roles_table, insert_role_sql
from main.model.user import User, Role

load_dotenv()

db_path = os.getenv('DATABASE_PATH')


def db_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        raise Error(e)  # todo - create error - db_connection_failed


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        raise Error(e)


def create_db_with_default_vales():
    conn = db_connection()
    if not conn:
        raise Error
    try:
        cur = conn.cursor()
        cur.execute(create_users_table)
        cur.execute(create_roles_table)
        cur.execute(create_users_roles_table)
        print("All table has been init")
        roles: list[Role] = list(Role)
        for role in roles:
            role_id = uuid.uuid4()
            print(f"Role {role_id}: {role.name}")
            cur.execute(insert_role_sql, (str(role_id), role.name,))
            print("Czy tu jest ok - po execute, przed commit")
            conn.commit()
            print("Czy tu jest ok - po commit")
    except sqlite3.Error as e:
        print(f"Tu jestem {e}")
        raise Error(e)
    finally:
        conn.close()


def find_all(table_name: str) -> list:
    conn = db_connection()
    if not conn:
        raise Error
    # todo - find if table exist in db
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        return rows if rows else []
    except sqlite3.Error as e:
        raise Error(e)
    finally:
        conn.close()


def find_by_id(record_id: str, table_name: str) -> list:
    conn = db_connection()
    if not conn:
        raise Error
    # todo - find if table exist in db
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE id = ?", record_id)
        rows = cur.fetchall()
        return rows if rows else []
    except sqlite3.Error as e:
        raise Error(e)
    finally:
        conn.close()


def find_by_parameter(record_parameter, table_name: str, parameter_name: str) -> list:
    conn = db_connection()
    if not conn:
        raise Error
    # todo - find if table exist in db
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {parameter_name} = ?", (record_parameter,))
        rows = cur.fetchall()
        return rows if rows else []
    except sqlite3.Error as e:
        raise Error(e)
    finally:
        conn.close()


def check_if_exist_by_parameter(record_parameter, table_name: str, parameter_name) -> bool:
    # todo - function checking if record exist
    conn = db_connection()
    if not conn:
        raise Error
    # todo - find if table exist in db
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {parameter_name} = ?", (record_parameter,))
        rows = cur.fetchall()
        cur.close()
        return True if rows else False
    except sqlite3.Error as e:
        raise Error(e)
    finally:
        conn.close()


def add_user_to_db(user: User):
    conn = db_connection()
    create_db_with_default_vales()  # todo - checking if tables exist
    if not conn:
        raise Error
    if not isinstance(user, User):
        raise ValueError("Invalid user object or missing user attribute.")
    try:
        if check_if_exist_by_parameter(str(user.id),
                                       TABLE_USERS,
                                       "id") or check_if_exist_by_parameter(str(user.email),
                                                                            TABLE_USERS,
                                                                            "email"):
            print("User with given id or email has already existed")
            raise Error
        else:
            cur = conn.cursor()
            cur.execute(insert_user_sql, (str(user.id), user.name, user.surname, user.email, user.password))
            conn.commit()
            cur.close()
    except Error as e:
        raise e
    finally:
        conn.close()
