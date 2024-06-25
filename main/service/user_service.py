import uuid
from main.const.database_const import TABLE_USERS
from main.const.global_const import ADD_RECORD_TO_DATABASE, RECORD_NOT_ADDED_TO_DATABASE, NOT_FOUND, EXCEPTION_HANDLE, \
    FOUND_RECORD_IN_DATABASE, DATA_CANNOT_GET_FROM_DATABASE
from main.data_base.db_repository import find_all, db_connection, find_by_parameter
from main.data_base.user_repository import add_user_to_db, find_user_by_id, find_roles_for_user
from main.exception.basic_exception import BasicException
from main.exception.database_conection_failed_exception import DatabaseConnectionFailedException
from main.login.password_analysis import hash_password
from main.mapper.user_mapper import map_user_tuple_to_user_class, map_roles_tuple_to_roles_set
from main.model.user import User, Role


def add_new_user(new_user: dict) -> dict:
    password = hash_password(new_user['password'])
    user = User(user_id=None,
                name=new_user['name'],
                surname=new_user['surname'],
                email=new_user['email'],
                password=password,
                roles={Role.READER})
    conn = db_connection()
    try:
        if not conn:
            raise DatabaseConnectionFailedException()
        add_user_to_db(conn, user)
        print(f"User with id = {user.id} has been added to database.")  # todo - log
        response = {
            "response_type": ADD_RECORD_TO_DATABASE,
            "message": f"New user with id = {user.id} has been added to database",
            "http_status_code": 201
        }
        return response
    except BasicException as e:
        response = {
            "response_type": RECORD_NOT_ADDED_TO_DATABASE,
            "message": f"New user with id = {user.id} has not been added to database",
            "http_status_code": 400
        }
        print(e)
        return response
    finally:
        conn.close()


def get_user_by_id_from_db(user_id: uuid) -> dict:
    conn = db_connection()
    try:
        if not conn:
            raise DatabaseConnectionFailedException()
        user_tuple, roles_tuple = find_user_by_id(conn, user_id)
        roles_set = map_roles_tuple_to_roles_set(roles_tuple)
        user = map_user_tuple_to_user_class(user_tuple, roles_set)
        user_message = user.to_dict()
        response = {
            "response_type": FOUND_RECORD_IN_DATABASE,
            "message": f"User with id = {user_id} has been found in database",
            "http_status_code": 200,
            "user": user_message
        }
        return response
    except BasicException as e:
        response = {
            "response_type": NOT_FOUND,
            "message": f"New user with id = {user_id} was not found in database",
            "http_status_code": 404
        }
        print(e)
        return response
    finally:
        conn.close()


def get_all_users() -> dict:
    conn = db_connection()
    try:
        if not conn:
            raise DatabaseConnectionFailedException()
        users_list = find_all(conn, TABLE_USERS)
        users = {map_user_tuple_to_user_class(user, map_roles_tuple_to_roles_set(find_roles_for_user(conn, user[0])))
                 for user in users_list}
        users_dict = list()
        for user in users:
            users_dict.append(user.to_dict())
        response = {
            "response_type": FOUND_RECORD_IN_DATABASE,
            "message": f"Users have been got in database",
            "http_status_code": 200,
            "users": users_dict
        }
        return response
    except BasicException as e:
        response = {
            "response_type": DATA_CANNOT_GET_FROM_DATABASE,
            "message": f"Users cannot be get from database, exception/error: {e}",
            "http_status_code": 404
        }
        print(e)
        return response
    finally:
        conn.close()
