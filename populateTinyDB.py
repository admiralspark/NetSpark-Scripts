"""
-------------------------------------------------------------------------------
This script takesinput from a CSV file, specifically Solarwinds, and stores
the information in a TinyDB database. This will be the first step in converting
to using TinyDB: getting the data IN the database.
-------------------------------------------------------------------------------

"""
from tinydb import TinyDB, Query
from datetime import datetime
import csv, os.path
import codecs

# Begin timing the script
start_time = datetime.now()

# Define the Database
db = TinyDB('netspark.json')

# Point it at the CSV file
# filename = raw_input("Name of the CSV file to import: ")
filename = "exportCP.csv"

# Function pop() will parse the SW config file and add it to our TinyDB
def pop():
    # Use codecs to parse utf-16...thanks Solarwinds for sucking so hard
    reader = csv.reader(codecs.open(filename, 'rU', 'utf-16'))
    # Skip the headers
    next(reader, None)
    # Define variable to "" for if statement, otherwise it is unbound
    devicetype = ""
    # Now iterate through every row in the CSVfile and make dictionaries
    for row in reader:
        if row[2] == 'Cisco':
            devicetype = "cisco_ios"
        switch = {
            'hostname': row[1],
            'ip': row[0],
            'device_type': devicetype,
            'customer_name': row[3],
        }
        dbf = Query()
        if db.search(dbf.ip == row[0]) != "":
            print "Skipping " + row[0] + " as it already exists."
        else:
            db.insert(switch)

pop()

# Kill the clock!
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
