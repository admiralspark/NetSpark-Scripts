'''
-------------------------------------------------------------------------------
This function loads the credentials from a CSV file for connecting to your
devices. Will hopefully become an *option* in the future instead of the only
one supported.
-------------------------------------------------------------------------------
'''

import csv, os.path

#Read in the credentials from file
def cred_csv():
    with open('credentials.csv', mode='r') as credfile:
        reader = csv.DictReader(credfile)
        for row in reader:
            username = row['username']
            password = row['password']
            secret = row['secret']
        return (username, password, secret)
