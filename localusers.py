'''
This script logs in to switches, checks the existing local usernames against
the allowed list, and remediates them if inconsistencies are found.
'''

#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

# Begin timing Script
start_time = datetime.now()

def lu (username, password, secret):
    with open(customer, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)

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

            net_connect = ConnectHandler(**switch)
            # command_string_mac = 'show mac add | inc ' + str(macAddr)
            # macreturn = net_connect.send_command(command_string_mac)

            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['SysName'])
            
            print "\n>>>>>>>>> End <<<<<<<<<"

            net_connect.disconnect()

# Grab the Customer name to search
customer = raw_input('Customer name: ') + ".csv"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Run the primary function in this program
lu(username, password, secret)

end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
