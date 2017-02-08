"""
-------------------------------------------------------------------------------
This script takesinput from a CSV file, specifically Solarwinds, and stores
the information in a TinyDB database. This will be the first step in converting
to using TinyDB: getting the data IN the database.
-------------------------------------------------------------------------------

"""
# External
from tinydb import TinyDB, Query
from datetime import datetime
import csv, os.path
import codecs
# Local
import convencoding

# Begin timing the script
start_time = datetime.now()

# Define the Database
db = TinyDB('netspark.json')

# Point it at the CSV file
#filename = raw_input("Name of the CSV file to import: ")
filename = "ASA.csv"
# Function populate() will parse the SW config file and add it to our TinyDB
def populate():
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
    # Now iterate through every row in the CSVfile and set variables
        for row in reader:
            ip = row['IP_Address']
            hostname = row['SysName']
            device_type = row['device_type']
            department = row['Department']
            switch = {
                'ip': row['IP_Address'],
                'hostname': row['SysName'],
                'device_type': row['device_type'],
                'department': row['Department']
            }

            dbf = Query()
            resultf = db.search(dbf.ip == row['IP_Address'])
            if str(resultf) != "[]":
                print "Skipping " + row['IP_Address'] + " as it already exists."
            else:
                db.insert(switch)
                print "Added " + row['IP_Address']

populate()

# Kill the clock!
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
