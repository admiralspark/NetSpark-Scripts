#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

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
            # Insert enables et al here
            # net_connect.enable()
            command_string = "write mem"
            connect_return = net_connect.send_command(command_string)
            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['SysName'])
            print connect_return
            print "\n>>>>>>>>> End <<<<<<<<<"
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
customer = raw_input('Customer name: ') + ".csv"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Run the primary function in this program
nc(username, password, secret)

end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
