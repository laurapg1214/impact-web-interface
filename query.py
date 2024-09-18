import owb_module_base.owb_module.owb as owb


def main():
    # connect to owb database
    connection = owb.create_db_connection(
        "localhost", 
        "laurapg1214", 
        "0bjectDataba$3",
        "users"
    )

    # create query
    query = """
    INSERT INTO accounts (
        username, 
        password_hash, 
        salt,
        hash_algo,
        iterations
        )
        VALUES
        (
        %s,
        %s,
        %s,
        %s,
        %s
        );
    """

    owb.execute_query(connection, query)


if __name__ == "__main__":
    main()