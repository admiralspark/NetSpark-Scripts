'''
This Script will log in to multiple devices, search their
MAC address tables, and spit out the ports those MAC's are
found on with the switch name. The idea is that it will
assist in finding the correct port for phones and other things.
'''

from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path

customer = raw_input('Customer name: ') + ".csv"
start_time = datetime.now()

with open('credentials.csv', mode='r') as credfile:
    reader = csv.DictReader(credfile)
    for row in reader:
        global username
        global password
        global secret
        username = row['username']
        password = row['password']
        secret = row['secret']

with open(customer, mode='r') as csvfile:
    reader = csv.DictReader(csvfile)
    macAddr = raw_input('MAC of the device in cisco format: \n')
    command_string = 'show mac add | inc ' + str(macAddr)
    for row in reader:
        hostname = row['hostname']
        device_type = row['device_type']
        ip = row['ip']
        switch = {
        'device_type': device_type,
        'ip': ip,
        'username': username,
        'password': password,
        'secret': secret,
        'verbose': False,
        }
        net_connect = ConnectHandler(**switch)
        output = net_connect.send_command(command_string)
        print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['hostname'])
        print output
        print ">>>>>>>>> End <<<<<<<<<"
        net_connect.disconnect()

end_time = datetime.now()
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
