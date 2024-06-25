import sqlite3
import uuid
from sqlite3 import Connection, Error
from dotenv import load_dotenv
import os

from main.const.database_const import TABLE_ROLES, TABLE_CATEGORIES, TABLE_STATUSES
from main.data_base.database_sql_statements import create_roles_table, insert_role_sql
from main.exception.basic_exception import BasicException
from main.exception.database_conection_failed_exception import DatabaseConnectionFailedException
from main.exception.db_error_exception import DatabaseErrorException
from main.exception.not_found_exception import NotFoundException
from main.exception.query_execute_failed_exception import QueryExecuteFailedException
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
        print(f"Table {table_name} has  {number_of_elements} elements.")
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


def find_all(conn: Connection, table_name: str) -> list:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        cur.close()
        return rows if rows else []
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


def find_by_parameter(conn: Connection, record_parameter, table_name: str, parameter_name: str) -> list:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name} WHERE {parameter_name} = ?", (record_parameter,))
        rows = cur.fetchall()
        return rows if rows else []
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def is_exist_by_parameter(conn: Connection, record_parameter, table_name: str, parameter_name: str) -> bool:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, table_name):
        raise NotFoundException(name=f"Table {table_name}")
    try:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {parameter_name} = ?", (record_parameter,))
        number_of_elements = cur.fetchone()[0]
        cur.close()
        print(f"Check {parameter_name}, number of elements {number_of_elements}")
        return False if number_of_elements == 0 else True
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def fill_enum_table(conn: Connection, table_name: str):
    print(f"Enum table name = {TABLE_ROLES} has not exist yet or is empty. It will be init or fill now.")
    if table_name == TABLE_ROLES:
        create_table(conn, create_roles_table, TABLE_ROLES)
        roles: list[Role] = list(Role.__members__.values())
        for role in roles:
            add_role_to_db(conn, role.name)

    elif table_name == TABLE_CATEGORIES:
        print(f"Table {table_name} will not be created right now")
        pass
    elif table_name == TABLE_STATUSES:
        print(f"Table {table_name} will not be created right now")
        pass
    else:
        print(f"Table {table_name} is not enum table.")
        # todo - is here need an exception?


def add_role_to_db(conn: Connection, role_name: str):
    if not conn:
        raise DatabaseConnectionFailedException()
    try:
        cur = conn.cursor()
        role_id = uuid.uuid4()
        print(f"Role {role_id}: {role_name}")
        cur.execute(insert_role_sql, (str(role_id), role_name))
        conn.commit()
        print(f"New role id = {role_id}, name = {role_name} has been saved in db")
        cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")
