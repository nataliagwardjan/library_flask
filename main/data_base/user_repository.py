import uuid

from main.const.database_const import TABLE_USERS, TABLE_ROLES, TABLE_USERS_ROLES
from main.data_base.database_sql_statements import insert_user_sql, insert_user_role_sql, create_users_table, \
    create_users_roles_table
from main.data_base.db_repository import is_exist_by_parameter, find_by_parameter, is_table_exists, \
    create_table, fill_enum_table, is_table_empty, find_by_id
from main.exception.already_exist_exception import AlreadyExistedException
from main.exception.basic_exception import BasicException
from main.exception.database_conection_failed_exception import DatabaseConnectionFailedException
from main.exception.db_error_exception import DatabaseErrorException
from main.exception.not_found_exception import NotFoundException
from main.exception.query_execute_failed_exception import QueryExecuteFailedException
from main.model.user import User
from sqlite3 import Connection, Error


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
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def add_user_roles_to_db(conn: Connection, user_id: uuid, role_name: str):
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, TABLE_USERS):
        print(f"Table {TABLE_USERS} has not exist yet. It will be init now.")
        create_table(conn, create_users_table, TABLE_USERS)
    if (not is_table_exists(conn, TABLE_ROLES)) or is_table_empty(conn, TABLE_ROLES):
        print(f"Table {TABLE_ROLES} has not exist yet. It will be init now.")
        fill_enum_table(conn, TABLE_ROLES)
    try:
        role_from_db = find_by_parameter(conn, role_name, TABLE_ROLES, 'name')
        if not role_from_db or len(role_from_db) > 1:
            print(f"Role {role_name} does not exist or there are more then one "
                  f"({len(role_from_db)}) role with that name")
            raise NotFoundException(name=f"Role {role_name}")
        else:
            role_id = role_from_db[0][0]
            user_role_id = uuid.uuid4()
            if not is_table_exists(conn, TABLE_USERS_ROLES):
                print(f"Table {TABLE_USERS_ROLES} has not exist yet. It will be init now.")
                create_table(conn, create_users_roles_table, TABLE_USERS_ROLES)
            cur = conn.cursor()
            cur.execute(insert_user_role_sql, (str(user_role_id), str(user_id), role_id,))
            conn.commit()
            cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def find_user_by_id(conn: Connection, user_id: uuid) -> (tuple, list[tuple]):
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, TABLE_USERS):
        print(f"Table {TABLE_USERS} has not exist.")
        raise NotFoundException(name=f"Table {TABLE_USERS}")
    if not is_table_exists(conn, TABLE_USERS_ROLES):
        print(f"Table {TABLE_USERS_ROLES} has not exist.")
        raise NotFoundException(name=f"Table {TABLE_USERS_ROLES}")
    if not is_table_exists(conn, TABLE_ROLES):
        print(f"Table {TABLE_ROLES} has not exist.")
        raise NotFoundException(name=f"Table {TABLE_ROLES}")
    try:
        user_from_db = find_by_id(conn, str(user_id), TABLE_USERS)
        if not user_from_db or len(user_from_db) > 1:
            print(f"User with id = {user_id} does not exist or there are more then one ({len(user_from_db)}) "
                  f"user with that id")
            raise NotFoundException(index=user_id, name="User")
        else:
            user_tuple = user_from_db[0]
            user_roles_from_db = find_by_parameter(conn, str(user_id), TABLE_USERS_ROLES, 'user_id')
            if not user_roles_from_db:
                print(f"Roles for user with id = {user_id} does not exist.")
                raise NotFoundException(index=user_id, name="Roles for user")
            list_of_roles_tuple = []
            print(f"user_roles_from_db = {user_roles_from_db}")
            for item in user_roles_from_db:
                print(f"Item = {item}")
                role_tuple = find_by_id(conn, item[2], TABLE_ROLES)
                if not role_tuple:
                    print(f"Roles with id = {item[2]} does not exist.")
                    raise NotFoundException(index=item[2], name="Role")
                else:
                    list_of_roles_tuple.append(role_tuple[0])
                    print(f"Current list_of_role_tuple = {list_of_roles_tuple}")
            return user_tuple, list_of_roles_tuple
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")
