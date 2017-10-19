'''
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
'''
import logging
import csv
from tinydb import TinyDB, Query

# Set logging level https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3 
logging.basicConfig(level=logging.DEBUG)

# Define the Database
DB = TinyDB('netspark.json')

# The test file (should be import from ini)
CSVFILE = 'test.csv'

# The Magic (read CSV as dict, form dict with data we care about, dump it into db)
with open(CSVFILE, mode='r') as csvfile:
    READER = csv.DictReader(csvfile)
    # Now iterate through every row in the CSVfile and make dictionaries
    for row in READER:
        dbdict = {
            'hostname': row['SysName'],
            'device_type': row['device_type'],
            'ipaddr': row['IP_Address'],
            'department': row['Department']
        }

        Find = Query()
        ifexists = DB.contains(Find.ipaddr == dbdict['ipaddr'])
        if ifexists is True:
            DB.update({'hostname': dbdict['hostname']}, Find.ipaddr == dbdict['ipaddr'])
            DB.update({'device_type': dbdict['device_type']}, Find.ipaddr == dbdict['ipaddr'])
            DB.update({'department': dbdict['department']}, Find.ipaddr == dbdict['ipaddr'])
            logging.debug("Updated DB with values: " + str(dbdict))
        else:
            DB.insert(dbdict)
            logging.debug("Added new values: " + str(dbdict))
