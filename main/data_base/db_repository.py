import sqlite3
import uuid
from sqlite3 import Connection, Error
from typing import Any

from dotenv import load_dotenv
import os

from main.const.database_const import TABLE_ROLES, TABLE_CATEGORIES, TABLE_STATUSES
from main.data_base.database_sql_statements import create_roles_table, insert_role_sql, insert_category_sql, \
    insert_status_sql
from main.exception.exception import BasicException
from main.exception.exception import DatabaseConnectionFailedException
from main.exception.exception import DatabaseErrorException
from main.exception.exception import NotFoundException
from main.exception.exception import QueryExecuteFailedException
from main.model.copy import Status
from main.model.title import Category
from main.model.user import Role

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
    except BasicException as e:
        raise DatabaseConnectionFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def is_table_exists(conn, table_name: str) -> bool:
    if not conn:
        raise DatabaseConnectionFailedException()
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        result = cur.fetchone()
        cur.close()
        return result is not None
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def is_table_empty(conn, table_name: str) -> bool:
    if not conn:
        raise DatabaseConnectionFailedException()
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name}")
        number_of_elements = cur.fetchone()[0]
        cur.close()
        return True if number_of_elements == 0 else False
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def create_table(conn: Connection, create_table_segment: str, table_name: str):
    if not conn:
        raise DatabaseConnectionFailedException()
    try:
        cur = conn.cursor()
        cur.execute(create_table_segment)
        print(f"Table {table_name} has been init")
        cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def find_all(conn: Connection, table_name: str) -> Any | None:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        cur.close()
        return rows[0] if rows else None
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def find_by_id(conn: Connection, record_id: str, table_name: str) -> list:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE id = ?", (record_id,))
        rows = cur.fetchall()
        return rows if rows else []
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def find_by_parameter(conn: Connection, table_name: str, record_value, record_name: str) -> list:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {record_name} = ?", (record_value,))
        rows = cur.fetchall()
        return rows if rows else []
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def is_exist_by_parameter(conn: Connection, table_name: str, record_value, record_name: str) -> bool:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {record_name} = ?", (record_value,))
        number_of_elements = cur.fetchone()
        cur.close()
        return False if number_of_elements == 0 else True
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def delete_by_parameter(conn: Connection, table_name: str, record_value, record_name: str):
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {table_name} WHERE {record_name} = ?", (record_value,))
        conn.commit()
        print(f"Delete from {table_name} record where {record_name} = {record_value}")
        cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def fill_enum_table(conn: Connection):
    tables = [{
        "name": TABLE_ROLES,
        "type": Role
    },
        {
        "name": TABLE_CATEGORIES,
        "type": Category
    },
        {
        "name": TABLE_STATUSES,
        "type": Status
    }
    ]
    for table in tables:
        record_list = list()

    # todo - for all enum types create tabel and fill it

    if not is_table_exists(conn, TABLE_STATUSES) or is_table_empty(conn, TABLE_STATUSES):
        print(f"Enum table name = {TABLE_STATUSES} has not exist yet or is empty. It will be init or fill now.")
        # create statuses table
        create_table(conn, create_roles_table, TABLE_STATUSES)
        statuses = list[Status] = list(Status.__members__.values())
        # fill table of possible option of statuses
        for status in statuses:
            add_enum_record_to_db(conn=conn, sql_insert_comment=insert_status_sql, record_name=status.name)

    if not is_table_exists(conn, TABLE_STATUSES) or is_table_empty(conn, TABLE_STATUSES):
        print(f"Enum table name = {TABLE_STATUSES} has not exist yet or is empty. It will be init or fill now.")
        # create categories table
        create_table(conn, create_roles_table, TABLE_STATUSES)
        categories: list[Category] = list(Category.__members__.values())
        # fill table of possible option of category
        for category in categories:
            add_enum_record_to_db(conn=conn, sql_insert_comment=insert_category_sql, record_name=category.name)


def add_enum_record_to_db(conn: Connection, sql_insert_comment: str, record_name: str):
    if not conn:
        raise DatabaseConnectionFailedException()
    try:
        cur = conn.cursor()
        record_id = uuid.uuid4()
        cur.execute(sql_insert_comment, (str(record_id), record_name))
        conn.commit()
        print(f"New record: id = {record_id}, name = {record_name} has been saved in db")
        cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def create_enum_table_and_fill_it(conn: Connection, table_name: str, record_list: list):
    create_enum_table = f"""
    -- table
    CREATE TABLE IF NOT EXISTS {table_name} (
    id TEXT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
    );
    """
    insert_enum_record = f"""
    INSERT INTO {table_name} (id, name) VALUES (?, ?)
    """
    if not is_table_exists(conn, table_name) or is_table_empty(conn, table_name):
        print(f"Enum table name = {table_name} has not exist yet or is empty. It will be init or fill now.")
        # create statuses table
        create_table(conn=conn, create_table_segment=create_enum_table, table_name=table_name)
        # fill table of possible option of statuses
        for record in record_list:
            add_enum_record_to_db(conn=conn, sql_insert_comment=insert_enum_record, record_name=record.name)