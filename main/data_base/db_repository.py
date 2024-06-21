import sqlite3
from sqlite3 import Error, Connection
from dotenv import load_dotenv
import os

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
