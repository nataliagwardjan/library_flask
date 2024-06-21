import uuid

from main.const.database_const import TABLE_USERS
from main.data_base.db_repository import find_all
from main.model.model import User


def add_user(user: dict):
    pass


def get_user(user_id: uuid) -> dict:
    return {}


def get_users() -> dict:
    users_list = find_all(TABLE_USERS)
    for user in users_list:
        print(user)

    return {}