# Adapted from https://www.geeksforgeeks.org/hiding-and-encrypting-passwords-in-python/

import maskpass  # to hide the password
import base64  # to encode and decode the password
 
# dictionary with username as key & pw as value
dict = {}
 
# function to create password
def create_pw():
    print("\n========Create Account=========")
    name = input("Username : ")
     
    # masking password with prompt msg 'Password :'
    pwd = maskpass.askpass("Password : ")

    # encoding the entered password
    encpwd = base64.b64encode(pwd.encode("utf-8"))
 
    # appending username and password in dict
    dict[name] = encpwd  
    print(dict)


# function to return dict
def return_dict(dict):
    return dict
 

# function for sign-in
def sign_in():
    print("\n\n=========Login Page===========")
    name = input("Username : ")
     
    # masking password with prompt msg 'Password :'
    pwd = maskpass.askpass("Password : ")
     
    # encoding the entered password
    encpwd = base64.b64encode(pwd.encode("utf-8"))
 
    # fetching password with
    # username as key in dict
    password = dict[name]  
    if(encpwd == password):
        print("Successfully logged in.")
    else:
        print("Login Failed")
 
# calling function
create_pw()
sign_in()