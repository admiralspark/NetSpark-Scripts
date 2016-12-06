'''
This script will standardize on specific usernames and passwords to
make sure that everything, everywhere, has the same backup accounts.
'''

# Global
from netmiko import ConnectHandler
import csv, os.path
from datetime import datetime

# Local
import credentials

# Begin timing Script
start_time = datetime.now()

def nc(username, password, secret, customer, command_string):
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
            net_connect.enable()
            connect_return = net_connect.send_command_expect(command_string)
            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['SysName'])
            print connect_return
            print "\n>>>>>>>>> End <<<<<<<<<"
            net_connect.disconnect()


# Proper way
# customer = raw_input('Customer name: ') + ".csv"
customer = "HOME.csv"
# Load credentials
username, password, secret = credentials.cred_csv()
# Temp input until this is working
command_string = "sh run | inc username"
# Now call the function
nc(username, password, secret, customer, command_string)

#End the time counter
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
