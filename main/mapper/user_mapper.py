import uuid

from main.exception.wrong_data_fields_amount_exception import WrongDataFieldsAmountException
from main.exception.wrong_data_type_from_db import WrongDataTypeException
from main.model.user import User, Role


def map_user_tuple_to_user_class(user_tuple: tuple, roles: set[Role]) -> User | None:
    """
    function map user get from db as tuple to class User
    :param roles:
    :param user_tuple:
    :return: User or None
    """
    if len(user_tuple) == 5:
        try:
            user_id = uuid.UUID(user_tuple[0])
            user_name = str(user_tuple[1])
            user_surname = str(user_tuple[2])
            user_email = str(user_tuple[3])
            user_password = str(user_tuple[4])
            user = User(user_id=user_id,
                        name=user_name,
                        surname=user_surname,
                        email=user_email,
                        password=user_password,
                        roles=roles)
            return user
        except ValueError as e:
            print(f"Wrong data type in the value, {e}")
            raise WrongDataTypeException(f"{e}")
    else:
        print("User tuple has not correct length")
        raise WrongDataFieldsAmountException(f"User tuple has not correct length ({len(user_tuple)} not 5)")
