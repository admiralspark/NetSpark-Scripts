'''
-------------------------------------------------------------------------------
This Script will log in to multiple devices, search their
MAC address tables, and spit out the ports those MAC's are
found on with the switch name. The idea is that it will
assist in finding the correct port for phones and other things.
-------------------------------------------------------------------------------
'''

#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

start_time = datetime.now()

def findmac(username, password, secret):
    with open(customer, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        macAddr = input('MAC of the device in cisco format: ')

        command_string_mac = 'show mac add | inc ' + str(macAddr)
        command_string_cdp = 'show cdp neigh | inc ' + str(macAddr)

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
            macreturn = net_connect.send_command(command_string_mac)
            cdpreturn = net_connect.send_command(command_string_cdp)

            print("\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['SysName']))
            print("\nMAC Address Hits on this switch: ")
            print(macreturn)
            print("\nCisco Discovery Protocol Hits on this switch: ")
            if cdpreturn == "":
                print("No CDP results for this MAC")
            else:
                print(cdpreturn)
                cdplist = ' '.join(macreturn.split())
                port = cdplist.split(' ')[3]
                command_string_port = 'show run int ' + str(port)
                portreturn = net_connect.send_command(command_string_port)
                print("\nPort Configuration for matched CDP: ")
                print(portreturn)
            print("\n>>>>>>>>> End <<<<<<<<<")

            net_connect.disconnect()

# Grab the Customer name to search
customer = input('Customer name: ') + ".csv"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Run the primary function in this program
findmac(username, password, secret)

end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print("\nTotal time for script: \n" + str(total_time))
