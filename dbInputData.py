'''
    Usage:
        dbInputData.py
        dbInputData.py -h | --help
        dbInputData.py [--debug] [-i INPUT] [-o FILE]

    Options:
        -h, --help      Shows this menu.
        -d, --debug     Print debug information. This is the most verbose
                        option.
        -i INPUT        Input file [default: test.csv]
        -o FILE         TinyDB database to output to. [default: netspark.json]
'''

import logging
import csv
from tinydb import TinyDB, Query
from docopt import docopt


arguments = docopt(__doc__)

# Set logging level https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3 
if arguments['--debug'] == True:
    logging.basicConfig(level=logging.DEBUG)
    print("Arguments: \n" + str(arguments))
else:
    logging.basicConfig(level=logging.INFO)

# Define the Database
DB = TinyDB(arguments['-o'])
logging.info("Set TinyDB database to: " + str(arguments['-o']))
logging.debug("Loaded database: " + str(DB))

# The test file
CSVFILE = arguments['-i']
logging.info("Set CSV input file to: " + str(CSVFILE))

# The Magic (read CSV as dict, form dict with data we care about, dump it into db)
with open(CSVFILE, mode='r') as csvfile:
    logging.debug("Attempting load of CSVFILE into dictionary...")
    READER = csv.DictReader(csvfile)
    logging.debug("csv.DictReader load success")
    # Now iterate through every row in the CSVfile and make dictionaries
    for row in READER:
        logging.debug("Iterating through csv dictionary rows...")
        dbdict = {
            'hostname': row['SysName'],
            'device_type': row['device_type'],
            'ipaddr': row['IP_Address'],
            'department': row['Department']
        }
        logging.debug("Made the following dbdict: " + str(dbdict))

        Find = Query()
        logging.debug("Begin searching for IP Address using dbdict['ipaddr']")
        ifexists = DB.contains(Find.ipaddr == dbdict['ipaddr'])
        if ifexists is True:
            logging.debug("Found match for IP. Updating values...")
            DB.update({'hostname': dbdict['hostname']}, Find.ipaddr == dbdict['ipaddr'])
            DB.update({'device_type': dbdict['device_type']}, Find.ipaddr == dbdict['ipaddr'])
            DB.update({'department': dbdict['department']}, Find.ipaddr == dbdict['ipaddr'])
            logging.debug("Updated DB with values: " + str(dbdict))
        else:
            logging.debug("No match found for IP. Adding new DB entry...")
            DB.insert(dbdict)
            logging.debug("Added new values: " + str(dbdict))
