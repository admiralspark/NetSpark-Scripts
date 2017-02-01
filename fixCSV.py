'''
-------------------------------------------------------------------------------
This script is the basis for converting Solarwinds exportCP.csv files to
a useable format! In the future, this will be step one of two for importing
customer data into a local TinyDB
-------------------------------------------------------------------------------
'''
from datetime import datetime
import csv, os.path
import codecs
# Local
import convencoding

# Begin timing the script
start_time = datetime.now()

#The Solarwinds file
filename = "exportCP.csv"
#Use convencoding to convert the encoding
fixfile = convencoding.conv(filename)
print str(fixfile) + " file has been created."
# Point it at the CSV file
#fixfile = raw_input("Name of the CSV file to import: ") + ".csv"

with open(fixfile, mode='r') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    with open(fixfile, mode='wb') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['Vendor'] == "Cisco":
                row['Vendor'] = "cisco_ios"
            del row['sha1(Department)']
            writer.writerow(row)

# Kill the clock!
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
