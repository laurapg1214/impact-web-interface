# adapted from https://www.askpython.com/python/examples/storing-retrieving-passwords-securely

import base64
import hashlib
import maskpass
import secrets


PEPPER = "0bj3ct$!Npw$"


def hash_password(password):    
    # generate cryptographically-secure 16 byte (128 bit) random salt value
    salt = secrets.token_bytes(16)
    # use pbkdf2 to generate secure pw hash
    iterations = 100_000
    hash_value = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8') + PEPPER.encode('utf-8'),
        salt,
        iterations
    )
    password_hash = hash_value + salt
    return password_hash







