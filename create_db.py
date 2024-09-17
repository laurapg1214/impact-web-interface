import owb_module_base.owb_module.database as db


def main():
    # create db connection
    connection = db.create_db_connection(
        "localhost", 
        "laurapg1214", 
        "0bjectDataba$3",
    )

    #create database
    create_database_query = "CREATE DATABASE owb"
    db.create_database(connection, create_database_query)



if __name__ == "__main__":
    main()

