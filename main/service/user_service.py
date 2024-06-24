import uuid
from main.const.database_const import TABLE_USERS
from main.const.global_const import ADD_RECORD_TO_DATABASE, RECORD_NOT_ADDED_TO_DATABASE
from main.data_base.db_repository import find_all, db_connection
from main.data_base.user_repository import add_user_to_db
from main.exception.basic_exception import BasicException
from main.exception.database_conection_failed_exception import DatabaseConnectionFailedException
from main.login.password_analysis import hash_password
from main.mapper.user_mapper import map_user_tuple_to_user_class
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



def get_user(user_id: uuid) -> dict:
    return {}


def get_users() -> dict:
    conn = db_connection()
    users_list = find_all(conn, TABLE_USERS)
    users = {map_user_tuple_to_user_class(user) for user in users_list}
    for user in users:
        print(user)
    users_dict = {user.to_dict() for user in users_list}
    return users_dict if users_dict else {}
