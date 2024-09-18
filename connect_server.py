import owb_module_base.owb_module.owb as owb


def main():
    # create db connection
    connection = owb.create_server_connection(
        "localhost", 
        "laurapg1214", 
        "0bjectDataba$3"
    )


if __name__ == "__main__":
    main()

