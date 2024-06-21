import uuid

from main.model.user import User, Role


def map_user_tuple_to_user_class(user_tuple: tuple) -> User | None:
    """
    function map user get from db as tuple to class User
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
            user = User(id=user_id,
                        name=user_name,
                        surname=user_surname,
                        email=user_email,
                        password=user_password,
                        roles={Role.READER})
            return user
        except ValueError as e:
            # todo - exception for wrong value type case
            print(f"Wrong data type in the value, {e}")
            return None
    else:
        # todo - exception for wrong tuple length
        print("User tuple has not correct length")
    return None
