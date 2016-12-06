'''
This script will standardize on specific usernames and passwords to
make sure that everything, everywhere, has the same backup accounts.
'''

# Global
from netmiko import ConnectHandler
import csv, os.path

# Local
import credentials

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
            connect_return = net_connect.send_command(command_string)
            print connect_return
            net_connect.disconnect()


# Proper way
# customer = raw_input('Customer name: ') + ".csv"
customer = "HOME.csv"
# Load credentials
username, password, secret = credentials.cred_csv()
# Temp input until this is working
command_string = "show version"
# Now call the function
nc(username, password, secret, customer, command_string)
