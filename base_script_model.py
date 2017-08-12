'''
This module is a base for single-thread scripts.
'''

#Global imports
from datetime import datetime
import csv
from netmiko import ConnectHandler
#Local imports
import credentials

# Begin timing the script
STARTTIME = datetime.now()

# Define the primary function (to be moved to a separate module some day...)
def netcon(username, password, secret, CUSTOMER, COMMANDSTRING):
    '''
    This is the core function. Iterates through a CSV, forms a dict, runs the command
    and logics it.
    '''
    with open(CUSTOMER, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        # Now iterate through every row in the CSVfile and make dictionaries
        for row in reader:
            hostname = row['SysName']
            device_type = row['device_type']
            ipaddr = row['IP_Address']
            switch = {
                'device_type': device_type,
                'ip': ipaddr,
                'username': username,
                'password': password,
                'secret': secret,
                'verbose': False,
            }
            # This is your connection handler for commands from here on out
            net_connect = ConnectHandler(**switch)
            # Insert your commands here
            net_connect.enable()
            # or maybe send configuration stuff with
            # net_connect.send_config_set(username cisco priv 15 pass cisco)
            connect_return = net_connect.send_command(COMMANDSTRING)
            # Now make it pretty
            print("\n\n>>>>>>>>> Device {0} {1} <<<<<<<<<".format(hostname, ipaddr))
            print(connect_return)
            print("\n>>>>>>>>> End <<<<<<<<<")
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
CUSTOMER = input('Customer name: ') + ".csv"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Just for testing
# COMMANDSTRING = input('Command string to run: ')
COMMANDSTRING = "show run | include hostname"
# Run the primary function in this program
netcon(username, password, secret, CUSTOMER, COMMANDSTRING)


ENDTIME = datetime.now()
# How long did it run?
TOTALTIME = ENDTIME - STARTTIME
print("\nTotal time for script: \n" + str(TOTALTIME))
