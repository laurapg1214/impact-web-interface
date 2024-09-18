import base64
import hashlib
import maskpass
import secrets


# adapted from https://www.askpython.com/python/examples/storing-retrieving-passwords-securely
def hash_password(password):    
    # generate cryptographically-secure 16 byte (128 bit) random salt value
    salt = secrets.token_bytes(16)
    password_hash = hashlib.sha256(password.encode() + salt)
    return password_hash.digest() + salt


password = input('Password: ')
print(hash_password(password))






