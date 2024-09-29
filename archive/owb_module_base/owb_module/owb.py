# owb library

# for database functions
import mysql.connector 
from mysql.connector import Error
import pandas as pd

# for password functions including create account & login
import hashlib
import maskpass
import secrets


##########################
### DATABASE FUNCTIONS ###
##########################

# adapted from https://www.freecodecamp.org/news/connect-python-with-sql/

def create_server_connection():  
    # close existing connections
    connection = None

    # handle potential errors
    try: 
        connection = mysql.connector.connect(
            host="localhost",
            user="owb_admin",
            password="0bjectDataba$3",
            database="owb"
        )
        print("MySQL connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    # if successful return MySQLConnection object
    return connection


# query execution 
def execute_query(connection, query, values=""):
    cursor = connection.cursor()
    try:
        cursor.execute(query, (values))
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


# password and user functions below adapted from https://www.askpython.com/python/examples/storing-retrieving-passwords-securely
# adaptations: extracted out functionality into password-specific/user-specific functions

##########################
### PASSWORD FUNCTIONS ###
##########################

# iterations & hash_algo for db
iterations = 100_000
# hash_algo = "PBKDF2"
hash_algo = "sha256"


def hash_password(password):
    # generate cryptographically-secure 16 byte (128 bit) random salt value
    salt = secrets.token_bytes(16)
    # use pbkdf2 to generate secure pw hash
    hash_value = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations
    )
    password_hash = salt + hash_value
    return password_hash


def get_password_hash(account, password):
    # extract info from user account
    key, salt, hash_algo, iterations = account[2:6]

    # recompute hash from user entered password
    password_hash = hashlib.pbkdf2_hmac(
        hash_algo,
        password.encode('utf-8'),
        salt,
        iterations
    )
    return password_hash, key


##############################
### USER ACCOUNT FUNCTIONS ###
##############################


def create_account():
    print("\n\n***CREATE ACCOUNT***")
    username = input("Username: ")
    password_hash = hash_password(maskpass.askpass("Password: "))
    
    # split hash into components
    salt, key = password_hash[:16], password_hash[16:]

    # insert user details into user_accounts table
    query = ("""
    INSERT INTO user_accounts (
        username, 
        password_hash,
        salt,
        hash_algo,
        iterations
        )
        VALUES
        (
        %s, %s, %s, %s, %s
        );
    """)

    values = (
        username,
        key,
        salt,
        hash_algo,
        iterations
    )

    # connect to owb database
    connection = create_server_connection()

    execute_query(connection, query, values)


def login():
    # connect to owb database
    connection = create_server_connection()

    # prompt user for login credentials
    print("\n\n***LOGIN***")
    username = input("Username: ")
    password = maskpass.askpass("Password: ")

    # check account
    query = """
    SELECT * FROM user_accounts WHERE username = %s
    """
    cursor = connection.cursor()
    cursor.execute(query, (username,))
    account = cursor.fetchone()

    if not account:
        print("Invalid username")
        return
    
    # send info to unhash_password function
    password_hash, key = get_password_hash(account, password)

    # compare hashes
    if password_hash == key:
        print("Login successful")
    else:
        print("Invalid password")



