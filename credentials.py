'''
-------------------------------------------------------------------------------
This function loads the credentials from a CSV file for connecting to your
devices. Will hopefully become an *option* in the future instead of the only
one supported.
-------------------------------------------------------------------------------
'''

import csv, os.path, getpass

#Read in the credentials from file
def cred_csv():
    if os.path.isfile('credentials.csv') == True:
        with open('credentials.csv', mode='r') as credfile:
            reader = csv.DictReader(credfile)
            for row in reader:
                username = row['username']
                password = row['password']
                secret = row['secret']
                return (username, password, secret)
    else:
        username = input("Username? ")
        password = getpass.getpass("Password? ")
        secret = getpass.getpass("Enable Password? ")
        return (username, password, secret)