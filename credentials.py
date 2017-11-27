'''
-------------------------------------------------------------------------------
This function loads the credentials from a CSV file for connecting to your
devices. Will hopefully become an *option* in the future instead of the only
one supported.
-------------------------------------------------------------------------------
'''

import csv
import os.path
import getpass

#Read in the credentials from file
def cred_csv(filename="credentials.csv"):
    """Check for existence of credentials file, read data if True, else ask for it manually"""
    if os.path.isfile(filename) is True:
        with open(filename, mode='r') as credfile:
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
'''
def cred_csv_key(keyname):
    if os.path.isfile('cred_keys.csv') is True:
        with open('cred_keys.csv', mode='r') as credkeys:
            reader = csv.DictReader(credkeys)
            for row in reader:
                if row['authentication'] is keyname:
                    username = row['username']
                    password = row['password']
                    secret = row['secret']
                    return (username, password, secret)
    else:
        print("cred_keys.csv missing, exiting")
        quit()
'''