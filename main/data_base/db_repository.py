import sqlite3
import uuid
from sqlite3 import Connection, Error

from dotenv import load_dotenv
import os

from main.const.database_const import TABLE_ROLES, TABLE_CATEGORIES, TABLE_STATUSES
from main.const.global_const import DATABASE_CONNECTION_FAILED, DATABASE_ERROR, EXCEPTION_HANDLE
from main.exception.exception import BasicException
from main.exception.exception import DatabaseConnectionFailedException
from main.exception.exception import DatabaseErrorException
from main.exception.exception import NotFoundException
from main.exception.exception import QueryExecuteFailedException
from main.model.copy import Status
from main.model.title import Category
from main.model.user import Role
from main.validator.database_validator import check_database_connection

load_dotenv()

db_path = os.getenv('DATABASE_PATH')


def db_connection() -> Connection:
    """ create a database connection to the SQLite database
        specified by db_file from .env
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except BasicException as e:
        print(f"{DATABASE_CONNECTION_FAILED.title()}. Exception/error: {e}")
        raise DatabaseConnectionFailedException(message=f"{e}")
    except Error as e:
        print(f"{DATABASE_ERROR.title()}. Exception/error = {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"{EXCEPTION_HANDLE.title()}. Exception/error = {e}")
        raise BasicException(message=f"{e}")


def is_table_exists(conn: Connection, table_name: str) -> bool:
    check_database_connection(conn)
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    try:
        cur = conn.cursor()
        cur.execute(query, (table_name,))
        result = cur.fetchone()
        cur.close()
        return result is not None
    except BasicException as e:
        print(f"Query '{query}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"{DATABASE_ERROR.title()}. Exception/error = {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"{EXCEPTION_HANDLE.title()}. Exception/error = {e}")
        raise BasicException(message=f"{e}")


def is_table_empty(conn: Connection, table_name: str) -> bool:
    check_database_connection(conn)
    query = f"SELECT COUNT(*) FROM {table_name}"
    try:
        cur = conn.cursor()
        cur.execute(query)
        number_of_elements = cur.fetchone()[0]
        cur.close()
        return True if number_of_elements == 0 else False
    except BasicException as e:
        print(f"Query '{query}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def create_table(conn: Connection, create_table_segment: str, table_name: str):
    check_database_connection(conn)
    try:
        cur = conn.cursor()
        cur.execute(create_table_segment)
        print(f"Table {table_name} has been init")
        cur.close()
    except BasicException as e:
        print(f"Query '{create_table_segment}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def find_all(conn: Connection, table_name: str) -> set:
    check_database_connection(conn)
    if not is_table_exists(conn, table_name):
        print(f"Table {table_name} has not existed. Select all record cannot be executed.")
        raise NotFoundException(message=f"Table {table_name} has not existed. Select all record cannot be executed.")
    query_select_all = f"SELECT * FROM {table_name}"
    try:
        cur = conn.cursor()
        cur.execute(query_select_all)
        rows = cur.fetchall()
        cur.close()
        return set(rows) if rows else set()
    except BasicException as e:
        print(f"Query '{query_select_all}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def find_by_parameter(conn: Connection, table_name: str, record_value, record_name: str) -> set:
    check_database_connection(conn)
    if not is_table_exists(conn, table_name):
        print(f"Table {table_name} has not existed. Data cannot be got.")
        raise NotFoundException(message=f"Table {table_name} has not existed. Data cannot be got.")
    query = f"SELECT * FROM {table_name} WHERE {record_name} = ?"
    try:
        cur = conn.cursor()
        cur.execute(query, (record_value,))
        rows = cur.fetchall()
        return set(rows) if rows else set()
    except BasicException as e:
        print(f"Query '{query}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def is_exist_by_parameter(conn: Connection, table_name: str, record_value, record_name: str) -> bool:
    check_database_connection(conn)
    if not is_table_exists(conn, table_name):
        print(f"Table {table_name} has not existed. Data cannot be got.")
        raise NotFoundException(message=f"Table {table_name} has not existed. Data cannot be got.")
    query = f"SELECT COUNT(*) FROM {table_name} WHERE {record_name} = ?"
    try:
        cur = conn.cursor()
        record_value = record_value if not isinstance(record_value, uuid.UUID) else str(record_value)
        cur.execute(query, (record_value,))
        number_of_elements = cur.fetchone()[0]
        cur.close()
        return False if number_of_elements == 0 else True
    except BasicException as e:
        print(f"Query '{query}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def delete_by_parameter(conn: Connection, table_name: str, record_value, record_name: str):
    check_database_connection(conn)
    if not is_table_exists(conn=conn, table_name=table_name):
        print(f"Table {table_name} has not existed. Data cannot be got.")
        raise NotFoundException(message=f"Table {table_name} has not existed. Data cannot be got.")
    if not is_exist_by_parameter(conn=conn, table_name=table_name, record_value=record_value, record_name=record_name):
        print(f"Record(s) with {record_name} = {record_value} has(have) not existed. Not possible to remove.")
        raise NotFoundException(
            message=f"Record(s) with {record_name} = {record_value} has(have) not existed. Not possible to remove.")
    query = f"DELETE FROM {table_name} WHERE {record_name} = ?"
    try:
        cur = conn.cursor()
        cur.execute(query, (record_value,))
        conn.commit()
        print(f"Delete from {table_name} record where {record_name} = {record_value}")
        cur.close()
    except BasicException as e:
        print(f"Query '{query}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def find_where_parameters(conn: Connection, table_name: str, **query: dict) -> set:
    """
    Query tasks from table with data from **query dict
    :param conn: the Connection object
    :param table_name: table name
    :param query: dict of attributes and values
    :return:
    """
    check_database_connection(conn)
    if not is_table_exists(conn=conn, table_name=table_name):
        print(f"Table {table_name} has not existed. Data cannot be got.")
        raise NotFoundException(message=f"Table {table_name} has not existed. Data cannot be got.")
    query_segments = []
    values = ()
    for key, value in query.items():
        query_segments.append(f"{key}=?")
        values += (value,)
    query_where = " AND ".join(query_segments)
    query_message = f"SELECT * FROM {table_name} WHERE {query_where}"

    try:
        cur = conn.cursor()
        cur.execute(query_message, (values,))
        cur.close()
        rows = cur.fetchall()
        return set(rows) if rows else set()
    except BasicException as e:
        print(f"Query '{query_message}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")


def create_enum_tables_and_fill_it(conn: Connection):
    tables = [
        {
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
        record_list = list(table['type'].__members__.values())
        create_enum_table_and_fill_it(conn=conn, table_name=table['name'], record_list=record_list)


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


def add_enum_record_to_db(conn: Connection, sql_insert_comment: str, record_name: str):
    check_database_connection(conn)
    try:
        cur = conn.cursor()
        record_id = uuid.uuid4()
        cur.execute(sql_insert_comment, (str(record_id), record_name))
        conn.commit()
        print(f"New record: id = {record_id}, name = {record_name} has been saved in db")
        cur.close()
    except BasicException as e:
        print(f"Query '{sql_insert_comment}' has not been executed in case of BasicException. Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")
