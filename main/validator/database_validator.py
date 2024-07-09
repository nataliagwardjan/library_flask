
from sqlite3 import Connection

from main.const.global_const import DATABASE_CONNECTION_FAILED
from main.exception.exception import DatabaseConnectionFailedException


def check_database_connection(conn: Connection):
    if not conn:
        print(f"{DATABASE_CONNECTION_FAILED.title()}.")
        raise DatabaseConnectionFailedException()
