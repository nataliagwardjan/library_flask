import uuid

from main.const.database_const import TABLE_USERS, TABLE_ROLES, TABLE_USERS_ROLES
from main.data_base.database_sql_statements import insert_user_sql, insert_user_role_sql, create_users_table, \
    create_users_roles_table, insert_role_sql
from main.data_base.db_repository import is_exist_by_parameter, find_by_parameter, is_table_exists, \
    create_table, fill_enum_table, is_table_empty, find_by_id
from main.exception.exception import AlreadyExistedException, BasicException, DatabaseConnectionFailedException, \
    DatabaseErrorException, NotFoundException, QueryExecuteFailedException
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
    if (not is_table_exists(conn, TABLE_ROLES)) or is_table_empty(conn, TABLE_ROLES):
        print(f"Table {TABLE_ROLES} has not exist yet. It will be init now.")
        fill_enum_table(conn)
    try:
        role_from_db = find_by_parameter(conn, TABLE_ROLES, role_name, 'name')
        if not role_from_db or len(role_from_db) > 1:
            print(f"Role {role_name} does not exist or there are more then one "
                  f"({len(role_from_db)}) role with that name")
            raise NotFoundException(name=f"Role {role_name}")
        else:
            role_id = role_from_db[0][0]
            print(f"Type of role_id = {type(role_id)}")
            if not is_table_exists(conn, TABLE_USERS_ROLES):
                print(f"Table {TABLE_USERS_ROLES} has not exist yet. It will be init now.")
                create_table(conn, create_users_roles_table, TABLE_USERS_ROLES)
            user_role_id = uuid.uuid4()
            cur = conn.cursor()
            cur.execute(insert_user_role_sql, (str(user_role_id), str(user_id), str(role_id)))
            conn.commit()
            cur.close()
            print(f"Role with id = {role_id} has been assigned to user {user_id}: "
                  f"user_role_id = {user_role_id}, user_id = {user_id}, role_id = {role_id}")
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
    try:
        user_from_db = find_by_id(conn, str(user_id), TABLE_USERS)
        if not user_from_db or len(user_from_db) > 1:
            print(f"User with id = {user_id} does not exist or there are more then one ({len(user_from_db)}) "
                  f"user with that id")
            raise NotFoundException(index=user_id, name="User")
        else:
            user_tuple = user_from_db[0]
            list_of_roles_tuple = find_roles_for_user_by_user_id(conn, user_id)
            return user_tuple, list_of_roles_tuple
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def find_roles_for_user_by_user_id(conn: Connection, user_id: uuid) -> set:
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, TABLE_USERS):
        raise NotFoundException(name=f"Table {TABLE_USERS}")
    if not is_table_exists(conn, TABLE_ROLES):
        raise NotFoundException(name=f"Table {TABLE_ROLES}")
    if not is_exist_by_parameter(conn, user_id, TABLE_USERS, "id"):
        raise NotFoundException(index=user_id, name=f"User")
    if not is_table_exists(conn, TABLE_USERS_ROLES):
        print(f"Table {TABLE_USERS_ROLES} not found")
        return set()
    try:
        cur = conn.cursor()
        select_roles_of_user_by_id_sql = f"""
        SELECT {TABLE_ROLES}.id, {TABLE_ROLES}.name FROM {TABLE_ROLES} 
        INNER JOIN {TABLE_USERS_ROLES} ON {TABLE_USERS_ROLES}.role_id = {TABLE_ROLES}.id 
        WHERE {TABLE_USERS_ROLES}.user_id = ?
        """
        cur.execute(select_roles_of_user_by_id_sql, (str(user_id),))
        rows = cur.fetchall()
        return set(rows) if rows else set()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


def remove_role_for_user(conn: Connection, user_id, role_id):
    if not conn:
        raise DatabaseConnectionFailedException()
    if not is_exist_by_parameter(conn, str(user_id), TABLE_USERS, "id"):
        raise NotFoundException(index=user_id, name=f"User")
    if not is_exist_by_parameter(conn, str(role_id), TABLE_ROLES, "id"):
        raise NotFoundException(index=role_id, name=f"Role")
    try:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM {TABLE_USERS_ROLES} WHERE user_id = ? and role_id = ?", (str(user_id), str(role_id),))
        conn.commit()
        cur.close()
    except BasicException as e:
        raise QueryExecuteFailedException(f"{e}")
    except Error as e:
        raise DatabaseErrorException(f"{e}")


