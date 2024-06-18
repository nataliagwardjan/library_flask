import random
import string

import bcrypt


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
    return ''.join(random.choice(password_characters) for i in range(16))
