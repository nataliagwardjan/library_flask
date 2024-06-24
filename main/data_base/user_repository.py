import uuid

from main.const.database_const import TABLE_USERS, TABLE_ROLES, TABLE_USERS_ROLES
from main.data_base.database_sql_statements import insert_user_sql, insert_user_role_sql, create_users_table, \
    create_users_roles_table
from main.data_base.db_repository import is_exist_by_parameter, find_by_parameter, is_table_exists, \
    create_table, fill_enum_table, is_table_empty
from main.exception.already_exist_exception import AlreadyExistedException
from main.exception.basic_exception import BasicException
from main.exception.database_conection_failed_exception import DatabaseConnectionFailedException
from main.exception.not_found_exception import NotFoundException
from main.exception.query_execute_failed_exception import QueryExecuteFailedException
from main.model.user import User
from sqlite3 import Connection


def add_user_to_db(conn: Connection, user: User):
    if not conn:
        raise DatabaseConnectionFailedException()
    if not isinstance(user, User):
        raise ValueError("Invalid user object or missing user attribute.")
    if not is_table_exists(conn, TABLE_USERS):
        print(f"Table {TABLE_USERS} has not exist yet. It will be init now.")
        create_table(conn, create_users_table, TABLE_USERS)
    try:
        if (is_exist_by_parameter(conn, str(user.id),
                                  TABLE_USERS,
                                  "id")
                or is_exist_by_parameter(conn, str(user.email),
                                         TABLE_USERS,
                                         "email")):
            print("User with given id or email has already existed")
            raise AlreadyExistedException(index=user.id, name="User")
        else:
            cur = conn.cursor()
            user_roles = user.roles
            for user_role in user_roles:
                add_user_roles_to_db(conn, user.id, user_role.name)
            cur.execute(insert_user_sql, (str(user.id), user.name, user.surname, user.email, user.password))
            conn.commit()
            cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")


def add_user_roles_to_db(conn: Connection, user_id: uuid, role_name: str):
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, TABLE_USERS):
        print(f"Table {TABLE_USERS} has not exist yet. It will be init now.")
        create_table(conn, create_users_table, TABLE_USERS)
    if (not is_table_exists(conn, TABLE_ROLES)) or is_table_empty(conn, TABLE_ROLES):
        print(f"Table {TABLE_USERS} has not exist yet. It will be init now.")
        fill_enum_table(conn, TABLE_ROLES)
    try:
        role_from_db = find_by_parameter(conn, role_name, TABLE_ROLES, 'name')
        if not role_from_db or len(role_from_db) > 1:
            print(
                f"Role {role_name} does not exist or there are more then one ({len(role_from_db)}) role with that name")
            raise NotFoundException(name=f"Role {role_name}")
        else:
            role_id = role_from_db[0][0]
            user_role_id = uuid.uuid4()
            cur = conn.cursor()
            if not is_table_exists(conn, TABLE_USERS_ROLES):
                print(f"Table {TABLE_USERS_ROLES} has not exist yet. It will be init now.")
                create_table(conn, create_users_roles_table, TABLE_USERS_ROLES)
            cur.execute(insert_user_role_sql, (str(user_role_id), str(user_id), role_id,))
            conn.commit()
            cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
