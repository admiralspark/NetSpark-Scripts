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
print(str(fixfile) + " file has been created.")

# Point it at the CSV file
with open(fixfile, mode='r') as f:
    reader = csv.DictReader(f)
    # Headers
    fieldnames = reader.fieldnames
    with open(fixfile, mode='wb') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        # Write Headers
        writer.writeheader()
        #Do some magic--change values to Netmiko compliance
        for row in reader:
            if row['Vendor'] == "Cisco":
                row['Vendor'] = "cisco_ios"
            # Don't need this row, I know it's dirty, this is not the end
            del row['sha1(Department)']
            writer.writerow(row)

# Stolen off the interwebz, to fix the improper dict tag (py2 has no replace
# for Dicts)
with open(fixfile) as f:
    vendfix = f.read().replace('Vendor', 'device_type')
    with open(fixfile, "w") as f:
        f.write(vendfix)


# Kill the clock!
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print("\nTotal time for script: \n" + str(total_time))
