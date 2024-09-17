import owb_module_base.owb_module.database as db
import owb_module_base.owb_module.password_encryption as pw


def main():
    dict = pw.create_pw()
    print(dict)

    # TODO: figure out how to replace username & pw below 
    # with dict values (pw decrypted)

    """# connect to owb database
    connection = db.create_db_connection(
        "localhost", 
        "laurapg1214", 
        "0bjectDataba$3",
        "owb"
    )"""


if __name__ == "__main__":
    main()