import owb_module_base.owb_module.owb as owb


def main():
    # connect to owb database
    connection = owb.create_server_connection()

    # create query
    query = """s
        CREATE TABLE events {
            id INT NOT NULL AUTO-INCREMENT,
            event_name VARCHAR(50) NOT NULL,
            organization
            PRIMARY KEY (id)
        }
        """

    owb.execute_query(connection, query)


if __name__ == "__main__":
    main()