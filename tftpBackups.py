'''
This script will verify TFTP backups on switches and remediate if
it's not working properly.
'''



#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

start_time = datetime.now()

def backups(username, password, secret, customer, tftp_ip):
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
            net_connect.enable()

            # Temporary variable, need raw input later
            change_number = "1"
            # Then command strings
            net_connect.send_command('send log "Starting change ticket {}"'.format(change_number))
            iphost = net_connect.send_command("sh run | inc ip host tftp")
            archive = net_connect.send_command("sh run | inc archive")
            kronpolicy = net_connect.send_command("sh run | inc kron policy-list BACKUP-CONFIG")
            kronoccur = net_connect.send_command("sh run | inc kron occurrence DAILY-CONFIG-BACKUP")

            print "\n\n>>>>>>>>> Device {0} <<<<<<<<<\n".format(row['SysName'])
            if iphost == "":
                net_connect.config_mode()
                ipcommand = "ip host tftp " + str(tftp_ip)
                net_connect.send_command_expect(ipcommand)
                print "Configured TFTP IP to " + str(tftp_ip)
            else:
                print "TFTP IP is already configured to " + str(iphost)
            if archive == "":
                config_archive = [  'archive',
                                    'path tftp://tftp/$h/$h',
                                    'write-memory',
                                    'exit' ]
                net_connect.send_config_set(config_archive)
                print "Archive now configured."
            else:
                print "Archive already configured."
            if kronpolicy == "":
                config_kronp = [    'kron policy-list BACKUP-CONFIG',
                                    'cli write memory',
                                    'exit'  ]
                net_connect.send_config_set(config_kronp)
                print "Kron Policy BACKUP-CONFIG now configured."
            else:
                print "Kron Policy BACKUP-CONFIG already configured."
            if kronoccur == "":
                config_krono = [    'kron occurrence DAILY-CONFIG-BACKUP at 0:05 recurring',
                                    'policy-list BACKUP-CONFIG',
                                    'exit']
                net_connect.send_config_set(config_krono)
                print "Kron Occurrence DAILY-CONFIG-BACKUP now configured."
            else:
                print "Kron Occurrence DAILY-CONFIG-BACKUP already configured."
            net_connect.send_command_expect('write memory')
            print "Memory Saved."
            net_connect.send_command('send log "Completing change ticket {}"'.format(change_number))
            print "\n>>>>>>>>> End <<<<<<<<<"
            # Disconnect from this session
            net_connect.disconnect()

# Grab the Customer name to search
customer = raw_input('Customer name: ') + ".csv"
# Grab the IP of the TFTP server to be sets
tftp_ip = raw_input('TFTP server IP: ')
# tftp_ip = "10.69.1.15"
# Flesh out these variables using the credentials.cred_csv module
username, password, secret = credentials.cred_csv()
# Run the primary function in this program
backups(username, password, secret, customer, tftp_ip)

end_time = datetime.now()
# How long did it run?
total_time = end_time - start_time
print "\nTotal time for script: \n" + str(total_time)
