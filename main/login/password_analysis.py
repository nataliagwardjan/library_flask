import random
import string
import re
import bcrypt

from main.const.global_const import MIN_PASSWORD_LENGTH, RANDOM_PASSWORD_LENGTH


def hash_password(password: str) -> str:
    # salt generator
    salt = bcrypt.gensalt()
    # hash password
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    # Base64 password
    return hashed_password.decode()


def check_password(password: str, hashed_password: str) -> bool:
    # check if password is correct
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def generate_random_password() -> str:
    password_characters = string.ascii_letters + string.punctuation + string.digits
    return ''.join(random.choice(password_characters) for _ in range(RANDOM_PASSWORD_LENGTH))


def is_valid_password(password: str) -> bool:
    f"""
    Checking if given password has:
    at least one lowercase letter
    at least one uppercase letter
    at least one digit
    at least one special character
    at least {MIN_PASSWORD_LENGTH} characters
    :param password:
    :return:
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?])[A-Za-z\d!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]{" + MIN_PASSWORD_LENGTH + ",}$"
    return bool(re.match(pattern, password))
