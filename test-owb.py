import owb_module_base.owb_module.database as db


def main():
    # create db connection
    connection = db.create_db_connection(
        "localhost", 
        "laurapg1214", 
        "2B0bjectDataba$3",
        "owb"
    )

    show_tables = """
    SHOW TABLES;
    """

    execute_query(connection, show_tables)


if __name__ == "__main__":
    main()

