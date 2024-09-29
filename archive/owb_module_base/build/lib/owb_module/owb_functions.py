import mysql.connector 
from mysql.connector import Error
import pandas as pd



def math_question(x, y):
    return x + y


# reusable db server connection code adapted from https://www.freecodecamp.org/news/connect-python-with-sql/
def create_db_server_connection(host_name, user_name, user_password):
    # close existing connections
    connection = None
    # handle potential errors
    try: 
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password
        )
        print("MySQL Database connection successful")
    except Error as error:
        print(f"Error: '{error}'")

    # if successful return MySQLConnection object
    return connection 


connection = create_db_server_connection("localhost", "laurapg1214", "2B0bjectDataba$3")
