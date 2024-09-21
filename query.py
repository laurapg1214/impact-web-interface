import owb_module_base.owb_module.owb as owb


def main():
    # connect to owb database
    connection = owb.create_server_connection(
        "localhost", 
        "laurapg1214", 
        "0bjectDataba$3",
        "owb"
    )

    # create query
    query = """ """

    owb.execute_query(connection, query)


if __name__ == "__main__":
    main()