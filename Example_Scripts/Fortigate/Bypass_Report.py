'''
This script will produce a report of the current whitelist objects of the input
address-group on the fortiOS appliance. 

    Usage:
        Bypass_Report.py -h | --help
        Bypass_Report.py [-o FILE] [--debug]
    
    Options:
        -h, --help          Shows this menu.
        -d, --debug         Print debug information. This is the most verbose
                            option.
        -o FILE             Output xlsx file [default: FW_Report.xlsx]
'''

import logging
import configparser
import xlsxwriter
from docopt import docopt
from netmiko import ConnectHandler

# Parse the .ini config file, this will let us set more permanent values
config = configparser.ConfigParser()
config.read("fortios.ini")
whitelist_name = config.get("fortios", "whitelist")

# Initialize docopt for arg parsing on the CLI
arguments = docopt(__doc__)

# Set logging level https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
# This is for debugging.
if arguments['--debug'] == True:
    logging.basicConfig(level=logging.DEBUG)
    print("Arguments: \n" + str(arguments))
else:
    logging.basicConfig(level=logging.WARNING)

# Initialize a Workbook object and add a new worksheet to it (for output)
workbook = xlsxwriter.Workbook(arguments['-o'])
worksheet = workbook.add_worksheet()
logging.info("Workbook " + str(arguments['-o']) + " loaded, and worksheet set...")

# Lists, declared globally is bad but it gets the job done
devices = []
ips = (config.get("fortios", "firewall_ip")).split(',')
rulename = []
comment = []
subset = []

# A hacky workaround for FortiOS not having a 'tree' view of firewall rules
def groupparse(addr):
    '''Use to parse down until you hit addresses, not addrgrps'''
    output = net_connect.send_command('show firewall addrgrp ' + str(addr) + ' | grep member')
    # Tidy data up
    output = output.split(' ')
    output = list(filter(None, output))
    output[-1] = output[-1].strip()
    output.remove('set')
    output.remove('member')
    for grp in output:
        newout = net_connect.send_command('show firewall address ' + str(grp) + ' | grep comment')
        if "Return code -163" in newout:
            # Recursive lookups
            rulename.append(grp)
            grpcom = net_connect.send_command('show firewall addrgrp ' + str(grp) + ' | grep comment')
            grpcom = grpcom[grpcom.find('"'):]
            comment.append(grpcom)
            subset.append("This is a GROUP")
            groupparse(newout)
        else:
            newout = newout[newout.find('"'):]
            # This only shows subset for the direct group, if we had 
            # nested groups it would not show the tree
            # print(grp, newout, "subset: " + str(addr))
            rulename.append(grp)
            comment.append(newout)
            subset.append(str(addr))

# Build connection dictionaries for each firewall you need to connect to
for ip in ips:
    logging.debug("Creating device dict for " + ip)
    fortinet = {
        'device_type': 'fortinet',
        'ip': ip,
        'username': str(config.get("fortios", "username")),
        'password': str(config.get("fortios", "password"))
    }
    devices.append(fortinet)
    logging.debug("Finished device dict:\n" + str(devices))

# Initial loop. This is a hack due to the FortiOS device not having a 'tree' 
# view of the firewall objects
for device in devices:
    logging.debug("Attempting connection to " + str(device['ip']))
    net_connect = ConnectHandler(**device)
    logging.debug("Sending command to " + str(device['ip']))
    output = net_connect.send_command('show firewall addrgrp ' + str(whitelist_name) + ' | grep member')
    # Tidy data up
    output = output.split(' ')
    output = list(filter(None, output))
    output[-1] = output[-1].strip()
    output.remove('set')
    output.remove('member')
    #print(output)
    for addr in output:
        newout = net_connect.send_command('show firewall address ' + str(addr) + ' | grep comment')
        if "Return code -163" in newout:
            rulename.append(addr)
            grpcom = net_connect.send_command('show firewall addrgrp ' + str(addr) + ' | grep comment')
            grpcom = grpcom[grpcom.find('"'):]
            comment.append(grpcom)
            subset.append("This is a GROUP")
            groupparse(addr)
        else:
            newout = newout[newout.find('"'):]
            #print(addr, newout)
            rulename.append(addr)
            comment.append(newout)
            subset.append(" ")

listoflists = {
    'Rule Names': rulename,
    'Comment': comment,
    'Group Membership': subset
}

# Change column width to make it readable. Not needed for import
# but it looks nicer this way for verification
worksheet.set_column(0, 0, width=50)
worksheet.set_column(1, 1, width=80)
worksheet.set_column(2, 2, width=50)

# This iterates over each key, writes the key out to the first row, and the 
# corresponding list in that column, per-key and per-column
colnum = 0
for key in listoflists.keys():
    worksheet.write(0, colnum, key)
    worksheet.write_column(1, colnum, listoflists[key])
    colnum += 1
    logging.debug("Added " + str(listoflists[key]))

# Close the open workbook i/o object
workbook.close()
logging.info("Closed Workbook " + str(arguments['-o']))