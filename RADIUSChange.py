#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

# Begin timing the script
start_time = datetime.now()

# Define the primary function (to be moved to a separate module some day...)
def nc(username, password, secret, customer, radiuskey, radiusserver, radiusgroupname, ticketnum):
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
            net_connect.enable()
            net_connect.send_command('send log "Beginning change ticket {}"'.format(ticketnum))
            aaanewmodel = net_connect.send_command('sh run | inc aaa new-model')
            oldradiusserver = net_connect.send_command('sh run | inc radius-server')
            oldaaaauth = net_connect.send_command('sh run | inc aaa authentication')
            oldVTYauth = net_connect.send_command('sh run | inc line vty|login authentication')
            oldgroup = net_connect.send_command('sh run | inc aaa group server radius ' + radiusgroupname)

            # or maybe send configuration stuff with
            # net_connect.send_config_set(username cisco priv 15 pass cisco)
            # Now make it pretty
            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<".format(row['SysName'])
            print "\n---------- Original Configuration ----------"
            print aaanewmodel
            print oldradiusserver
            print oldaaaauth
            print oldVTYauth
            if oldgroup != "":
                print oldgroup
            print "---------- Modified Configuration ------------\n"
            if aaanewmodel == "":
                net_connect.send_config_set('aaa new-model')
                print "New AAA model enabled on device"
            if oldgroup == "":
                config_radgroup = [ 'aaa group server radius ' + str(radiusgroupname),
                                    'server-private ' + str(radiusserver) + ' auth-port 1812 acct-port 1813 key ' + radiuskey,
                                    'exit',
                                    'aaa authentication login VTY local group ' + str(radiusgroupname),
                                    'end' ]
                net_connect.send_config_set(config_radgroup)
                #print config_radgroup
                print "AAA Group " + str(radiusgroupname) + " at IP " + str(radiusserver) + " configured on device"
            else:
                print "AAA group already configured on device"
            print "\n>>>>>>>>> End <<<<<<<<<"
            net_connect.send_command('send log "Completing change ticket {}"'.format(ticketnum))
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
customer = raw_input('Customer name: ') + ".csv"
# Enter ticket number for SW change logging
ticketnum = raw_input('Ticket #: ')
# Ask for the RADIUS key you want to username
radiuskey = raw_input('Enter the RADIUS key for authentication: ')
# And the RADIUS server
radiusserver = raw_input('Enter the RADIUS server: ')
# And your group name! (seriously just take all this from config)
radiusgroupname = raw_input('Enter the RADIUS group-name: ')
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Give it a command:
# command_string = "write mem" # can be passed to nc...
# Run the primary function in this program
nc(username, password, secret, customer, radiuskey, radiusserver, radiusgroupname, ticketnum)

# Script does the needful....

end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
