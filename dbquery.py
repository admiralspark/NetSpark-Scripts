"""
-------------------------------------------------------------------------------
This script just queries the database as a test for me. It can be used as an
example of how TinyDB queries can be done.
I'm just sick of typing it in the interpreter over and over.
-------------------------------------------------------------------------------
"""
from tinydb import TinyDB, Query

# Define the Database
DB = TinyDB('netspark.json')

# Construct additional pylons
IPADDR = input("What IP do you want to search for: ")

# Make the query
FINDIT = Query()
FRESULT = DB.search(FINDIT.ip == IPADDR)
print(FRESULT)
