'''
This program will back up the current running configuration to the TFTP server
of your choice. Honestly, you should use SFTP or SCP but, here we are. 
'''

#Global imports
from datetime import datetime
import csv
import configparser
from netmiko import ConnectHandler
#Local imports
import credentials

# Begin timing the script
STARTTIME = datetime.now()

config = configparser.ConfigParser()
config.read("netsparkconfig.ini")
tftpserver = config.get("tftpinfo", "tftpserver")

# Define the primary function (to be moved to a separate module some day...)
def netcon(username, password, secret, CUSTOMER):
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
            COMMANDSTRING = "copy running-config tftp://" + tftpserver + "/" + hostname + "-" + TODAYDATE + ".txt"
            config_archive = [  'file prompt quiet' ]
            net_connect.send_config_set(config_archive)
            checkbackup = net_connect.send_command(COMMANDSTRING)
            fix_archive = [  'file prompt alert' ]
            net_connect.send_config_set(fix_archive)

            # Now make it pretty
            print("\n\n>>>>>>>>> Device {0} {1} <<<<<<<<<".format(hostname, ipaddr))
            print(checkbackup)
            print("\n>>>>>>>>> End <<<<<<<<<")
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
CUSTOMER = input('Customer name: ') + ".csv"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Just for testing
# COMMANDSTRING = input('Command string to run: ')
TODAYDATE = str(datetime.now().date())
# Run the primary function in this program
netcon(username, password, secret, CUSTOMER)


ENDTIME = datetime.now()
# How long did it run?
TOTALTIME = ENDTIME - STARTTIME
print("\nTotal time for script: \n" + str(TOTALTIME))
