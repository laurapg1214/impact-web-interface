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


# db/server connection; db_name optional
def create_server_connection(host_name, user_name, user_password, db_name=""):
    # close existing connections
    connection = None
    # handle potential errors
    try: 
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        print("MySQL connection successful")
    except Error as error:
        print(f"Error: '{error}'")

    # if successful return MySQLConnection object
    return connection


# query execution 
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


##########################
### PASSWORD FUNCTIONS ###
##########################

# adapted from https://www.askpython.com/python/examples/storing-retrieving-passwords-securely
# create pepper for use across all hashed pws; iterations & hash_algo for db
iterations = 100_000
hash_algo = "PBKDF2"


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
    password_hash = hash_value + salt
    return password_hash


##############################
### USER ACCOUNT FUNCTIONS ###
##############################


def create_account():
    print("\n\n***CREATE ACCOUNT***")
    username = input("Username: ")
    password_hash = hash_password(maskpass.askpass("Password: "))
    return username, password_hash


def login()
    print("\n\n***LOGIN***")
    username = input("Username: ")
    password = maskpass.askpass("Password: ")


