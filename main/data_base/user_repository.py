import uuid

from main.const.database_const import TABLE_USERS, TABLE_ROLES, TABLE_USERS_ROLES
from main.const.global_const import DATABASE_CONNECTION_FAILED
from main.data_base.database_sql_statements import insert_user_sql, insert_user_role_sql, create_users_table, \
    create_users_roles_table
from main.data_base.db_repository import is_exist_by_parameter, find_by_parameter, is_table_exists, \
    create_table, create_enum_tables_and_fill_it, is_table_empty
from main.exception.exception import AlreadyExistedException, BasicException, DatabaseConnectionFailedException, \
    DatabaseErrorException, NotFoundException, QueryExecuteFailedException, ValueException
from main.model.user import User
from sqlite3 import Connection, Error


def add_user_to_db(conn: Connection, user: User):
    if not conn:
        print(f"{DATABASE_CONNECTION_FAILED.title()}.")
        raise DatabaseConnectionFailedException()
    if not isinstance(user, User):
        raise ValueException(message="Invalid user object or missing user attribute.")
    if not is_table_exists(conn, TABLE_USERS):
        print(f"Table {TABLE_USERS} has not exist yet. It will be init now.")
        create_table(conn, create_users_table, TABLE_USERS)
    try:
        if (is_exist_by_parameter(conn=conn, table_name=TABLE_USERS, record_value=user.id, record_name="id")
                or is_exist_by_parameter(conn=conn, table_name=TABLE_USERS, record_value=user.email,
                                         record_name="email")):
            print(f"User with given id ({user.id}) or email ({user.email}) has already existed.")
            raise AlreadyExistedException(
                message=f"User with given id ({user.id}) or email ({user.email}) has already existed.")
        else:
            print(f"New user is going to add to database: user = {user}")
            cur = conn.cursor()
            user_roles = user.roles
            for user_role in user_roles:
                add_user_roles_to_db(conn, user.id, user_role.name)
            cur.execute(insert_user_sql, (str(user.id), user.name, user.surname, user.email, user.password))
            conn.commit()
            cur.close()
    except BasicException as e:
        print(f"{e}")
        raise BasicException(exception_type=e.exception_type, message=e.message)
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def add_user_roles_to_db(conn: Connection, user_id: uuid, role_name: str):
    if not conn:
        print(f"{DATABASE_CONNECTION_FAILED.title()}.")
        raise DatabaseConnectionFailedException()
    if (not is_table_exists(conn, TABLE_ROLES)) or is_table_empty(conn, TABLE_ROLES):
        print(f"Table {TABLE_ROLES} has not exist yet. It will be init now.")
        create_enum_tables_and_fill_it(conn)
    try:
        role_from_db = find_by_parameter(conn=conn, table_name=TABLE_ROLES, record_value=role_name, record_name='name')
        if not role_from_db or len(role_from_db) > 1:
            print(f"Role {role_name} does not exist or there are more then one "
                  f"({len(role_from_db)}) role with that name")
            raise NotFoundException(message=f"Role {role_name} does not exist or there are more then one "
                                            f"({len(role_from_db)}) role with that name")
        else:
            (role, ) = role_from_db
            role_id = role[0]
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
        print(f"{e}")
        raise BasicException(exception_type=e.exception_type, message=e.message)
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def find_user_by_id(conn: Connection, user_id: uuid) -> (tuple, list[tuple]):
    if not conn:
        print(f"{DATABASE_CONNECTION_FAILED.title()}.")
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, TABLE_USERS):
        print(f"Table {TABLE_USERS} has not existed. User cannot be found.")
        raise NotFoundException(f"Table {TABLE_USERS} has not existed. User cannot be found.")
    try:
        user_from_db = find_by_parameter(conn=conn, table_name=TABLE_USERS, record_value=str(user_id), record_name="id")
        if not user_from_db or len(user_from_db) > 1:
            print(f"User with id = {user_id} does not exist or there are more then one ({len(user_from_db)}) "
                  f"user with that id")
            raise NotFoundException(message=f"User with id = {user_id} does not exist "
                                            f"or there are more then one ({len(user_from_db)}) user with that id")
        else:
            (user_tuple,) = user_from_db
            list_of_roles_tuple = find_roles_for_user_by_user_id(conn, user_id)
            return user_tuple, list_of_roles_tuple
    except BasicException as e:
        print(f"{e}")
        raise BasicException(exception_type=e.exception_type, message=e.message)
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def find_roles_for_user_by_user_id(conn: Connection, user_id: uuid) -> set:
    if not conn:
        print(f"{DATABASE_CONNECTION_FAILED.title()}.")
        raise DatabaseConnectionFailedException()
    if not is_table_exists(conn, TABLE_USERS):
        print(f"Table {TABLE_USERS} has not existed. User cannot be found.")
        raise NotFoundException(f"Table {TABLE_USERS} has not existed. Roles for user cannot be found.")
    if not is_table_exists(conn, TABLE_ROLES):
        print(f"Table {TABLE_ROLES} has not existed. User cannot be found.")
        raise NotFoundException(f"Table {TABLE_ROLES} has not existed. Roles cannot be found.")
    if not is_exist_by_parameter(conn=conn, table_name=TABLE_USERS, record_value=user_id, record_name="id"):
        print(f"User with id = {user_id} does not exist.")
        raise NotFoundException(message=f"User with id = {user_id} does not exist.")
    if not is_table_exists(conn, TABLE_USERS_ROLES):
        print(f"Table {TABLE_USERS_ROLES} not found")
        return set()
    select_roles_of_user_by_id_sql = f"""
            SELECT {TABLE_ROLES}.id, {TABLE_ROLES}.name FROM {TABLE_ROLES} 
            INNER JOIN {TABLE_USERS_ROLES} ON {TABLE_USERS_ROLES}.role_id = {TABLE_ROLES}.id 
            WHERE {TABLE_USERS_ROLES}.user_id = ?
            """
    try:
        cur = conn.cursor()
        cur.execute(select_roles_of_user_by_id_sql, (str(user_id),))
        rows = cur.fetchall()
        return set(rows) if rows else set()
    except BasicException as e:
        print(f"Query '{select_roles_of_user_by_id_sql}' has not been executed in case of BasicException."
              f" Exception/error: {e}")
        raise QueryExecuteFailedException(message=f"{e}")
    except Error as e:
        print(f"Error with database. Exception/error: {e}")
        raise DatabaseErrorException(message=f"{e}")
    except Exception as e:
        print(f"An exception has been handled. Exception/error: {e}")
        raise BasicException(message=f"{e}")


def remove_role_for_user(conn: Connection, user_id, role_id):
    if not conn:
        print(f"{DATABASE_CONNECTION_FAILED.title()}.")
        raise DatabaseConnectionFailedException()
    if not is_exist_by_parameter(conn, str(user_id), TABLE_USERS, "id"):
        print(f"User with id = {user_id} does not exist.")
        raise NotFoundException(message=f"User with id = {user_id} does not exist.")
    if not is_exist_by_parameter(conn, str(role_id), TABLE_ROLES, "id"):
        print(f"Role with id = {role_id} does not exist.")
        raise NotFoundException(message=f"Role with id = {role_id} does not exist.")
    query = f"DELETE FROM {TABLE_USERS_ROLES} WHERE user_id = ? and role_id = ?"
    try:
        cur = conn.cursor()
        cur.execute(query, (str(user_id), str(role_id),))
        conn.commit()
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
