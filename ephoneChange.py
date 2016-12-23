#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

# Begin timing the script
start_time = datetime.now()

# Define the primary function (to be moved to a separate module some day...)
def nc(username, password, secret, customercsv, i):
    with open(customercsv, mode='r') as csvfile:
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
            # Now make it pretty
            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<\n".format(row['SysName'])
            # Enable mode
			net_connect.enable()
            # Here's the commands to be run in config mode
			fix_call_waiting = [ i,
                                'no call-waiting beep',
                                'exit' ]
            # Send the fix
			net_connect.send_config_set(fix_call_waiting)
            # Make sure it's applied
			verify_config = "show run | beg {0}".format(i)
            con_ret = net_connect.send_command(verify_config)
            # Formatted to match all text before the first '!', due to sh run sucking hard
			print con_ret.partition("!")[0]
			# Now let everyone else know we're doing things (ELK is working, right?)
            sendlog = str('send log 0 "Added no call-waiting beep to {}"').format(i)
            net_connect.send_command(sendlog)
            print "\n>>>>>>>>> End <<<<<<<<<"
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
customer = raw_input('Customer name: ')
customercsv = str(customer) + ".csv"
ephone = str(customer) + "-ephone.txt"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Run the primary function in this program
with open(ephone, 'r') as inputfile:
    data=inputfile.readlines()
    for i in data:
        nc(username, password, secret, customercsv, i)

# Stop time!
end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
