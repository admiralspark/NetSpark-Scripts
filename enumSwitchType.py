#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

# Begin timing the script
start_time = datetime.now()

# Define the primary function (to be moved to a separate module some day...)
def enumSwitch(username, password, secret, customer):
    with open(customer, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        # Now iterate through every row in the CSVfile and make dictionaries
        for row in reader:
            hostname = row['SysName']
            device_type = row['device_type']
            ip = row['IP_Address']
            switch = {
                'device_type': device_type,
                'ip': ip,
                'username': username,
                'password': password,
                'secret': secret,
                'verbose': False,
            }
            # This is your connection handler for commands from here on out
            net_connect = ConnectHandler(**switch)
            # Insert your commands here
            # net_connect.enable()
            # or maybe send configuration stuff with
            # net_connect.send_config_set(username cisco priv 15 pass cisco)
            command_string = "show version | include Model number"
            connect_return = net_connect.send_command(command_string)
            # Now make it pretty
            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['SysName'])
            print connect_return
            print "\n>>>>>>>>> End <<<<<<<<<"
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
customer = raw_input('Customer name: ') + ".csv"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Give it a command:
# command_string = "write mem" # can be passed to nc...
# Run the primary function in this program
enumSwitch(username, password, secret, customer)


end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
