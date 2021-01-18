'''
This module is a base for single-thread scripts.
'''

#Global imports
from datetime import datetime
import csv, os.path, sys, getopt
from os import path
from netmiko import ConnectHandler
from getpass import getpass

# Get login credentials
username = input("Enter username: ")
password = getpass()
secret = getpass(prompt="Enter secret if required: ")
# Begin timing the script
STARTTIME = datetime.now()

# Define the primary function (to be moved to a separate module some day...)
def netcon(username, password, secret, CUSTOMER, COMMANDLIST, MODE):
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
            print("\n\n>>>>>>>>> Device {0} {1} <<<<<<<<<".format(hostname, ipaddr))
            if (MODE):
                for i in COMMANDLIST
                    connect_return = net_connect.send_config_set(COMMANDLIST)
                    print(connect_return)
            else:
                for i in COMMANDLIST:
                    connect_return = net_connect.send.command(COMMANDLIST)
                    print(connect_return)
            # Now make it pretty
            print("\n>>>>>>>>> End <<<<<<<<<")
            # Disconnect from this session
            net_connect.disconnect()

# Prompts for manual input or file input for commands
def GetOption (COMMANDLIST, Mode):
    CommandOption = input("(1) Enter commands manually\n(2) Enter filename containing commands:\t")
    while CommandOption != int(1 or 2):
        CommandOption = input("(1) Enter commands manually\n(2) Enter filename containing commands:\t")
    if CommandOption = 1:
        ManualCommands(COMMANDLIST)
    else if CommandOption = 2:
        FileCommands (COMMANDLIST)

# Prompts for user to input commands line by line
def ManualCommands (COMMANDLIST):
    command = input("Input one command per line, end with an extra newline: ")
    while command is not "":
        COMMANDLIST.append(command)
        command = input("Input one command per line, end with an extra newline: ")

# Prompts for file containing commands and checks that file exists
def FileCommands (COMMANDLIST):
    CommandFile = input("Enter path to command file (C:\\path\\to\\file): ")
    while path.exists(CommandFile) is False:
        CommandFile = input("Enter path to command file: ")
    if path.exists(CommandFile):
        with open(CommandFile) as f:
            COMMANDLIST = f.readline

# Prompts for for config mode or not
def CommandMode():
    choice = input("Are the commands for configuration (y/n) ")
    while choice != ('y' or 'n'):
        choice = input("Are the commands for configuration (y/n) ")
    if choice == 'y':
        MODE = True
    else if choice == 'n':
        MODE = False

# Grab the Customer name to search
CUSTOMER = input('Customer name: ') + ".csv"
# Flesh out these variables using the credentials.cred_csv module
# username, password, secret = credentials.cred_csv()
# Just for testing
#COMMANDSTRING = input('Command string to run: ')
COMMANDLIST = []



# Gets if running in config mode or not
CommandMode()

# Gets option of input for commands
GetOption(COMMANDLIST, MODE)

# Run the primary function in this program
netcon(username, password, secret, CUSTOMER, COMMANDLIST)


ENDTIME = datetime.now()
# How long did it run?
TOTALTIME = ENDTIME - STARTTIME
print("\nTotal time for script: \n" + str(TOTALTIME))
