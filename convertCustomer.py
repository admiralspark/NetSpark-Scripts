'''
-------------------------------------------------------------------------------
This script converts the encoding on Solarwinds csv's and will
eventually make them pretty and usable as a customer file as well.
Some day, it might even pull from a SW database!
-------------------------------------------------------------------------------
'''
from datetime import datetime
import csv, os.path
import codecs
# Local
import convencoding

# Begin timing the script
start_time = datetime.now()

# Point it at the CSV file
# filename = raw_input("Name of the CSV file to import: ")
# This is temporary I SWEAR...
filename = "exportCP.csv"
if filename == "exportCP.csv":
    fixfile = convencoding.conv(filename)
    print str(fixfile) + " file has been created."

# Kill the clock!
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
