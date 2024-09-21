# adapted from https://www.askpython.com/python/examples/storing-retrieving-passwords-securely

import owb_module_base.owb_module.owb as owb


# generate secure pw hash
username, password_hash = owb.create_account()


# split hash into components
salt, key = password_hash[:16], password_hash[16:]

# connect to owb database
connection = owb.create_server_connection(
    "localhost", 
    "laurapg1214", 
    "0bjectDataba$3",
    "owb"
)

# insert user details into user_accounts table
query = ("""
INSERT INTO user_accounts (
    username, 
    password_hash,
    salt,
    hash_algo,
    iterations
    )
    VALUES
    (
    %s, %s, %s, %s, %s
    );
""")

values = (
    username,
    key,
    salt,
    owb.hash_algo,
    owb.iterations
)

owb.execute_query(connection, query, values)

