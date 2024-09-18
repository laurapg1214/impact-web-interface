# adapted from https://www.askpython.com/python/examples/storing-retrieving-passwords-securely

import owb_module_base.owb_module.owb as owb


# generate secure pw hash
username, password_hash = owb.create_account()
print(username, password_hash)

# split hash into components
key, salt = password_hash[:16], password_hash[16:]

# insert into database
query = """"""

