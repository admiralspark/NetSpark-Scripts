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
filename = raw_input("Name of the CSV file to import: ")
# filename = "exportCP.csv"
if filename == "exportCP.csv":
    filename = convencoding.conv(filename)

# Function pop() will parse the SW config file and add it to our TinyDB
def pop():
    # Use codecs to parse utf-16...thanks Solarwinds for sucking so hard
    reader = csv.reader(codecs.open(filename, 'rU'))
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
        resultf = db.search(dbf.ip == row[0])
        if str(resultf) != "[]":
            print "Skipping " + row[0] + " as it already exists."
        else:
            db.insert(switch)
            print "Added " + row[0]

pop()

# Kill the clock!
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
