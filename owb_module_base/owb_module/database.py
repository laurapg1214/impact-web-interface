import mysql.connector 
from mysql.connector import Error
import pandas as pd

# functions below adapted from https://www.freecodecamp.org/news/connect-python-with-sql/

# db/server connection; db_name optional
def create_db_connection(host_name, user_name, user_password, db_name=''):
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
        print("MySQL Database connection successful")
    except Error as error:
        print(f"Error: '{error}'")

    # if successful return MySQLConnection object
    return connection

# create database 
def create_database(connection, query):
    # create cursor object
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


# query execution 
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")




# 





