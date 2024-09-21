# adapted from https://www.askpython.com/python/examples/storing-retrieving-passwords-securely


import owb_module_base.owb_module.owb as owb

# connect to owb database
connection = owb.create_server_connection(
    "localhost", 
    "laurapg1214", 
    "0bjectDataba$3",
    "owb"
)

owb.login(connection)

