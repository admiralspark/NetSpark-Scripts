'''
-------------------------------------------------------------------------------
This script is a baseline for multithreaded conversion of all of the scripts.
I'll look into converting the repo to use multithread, some day.
-------------------------------------------------------------------------------
'''

from datetime import datetime
import csv
import configparser
from multiprocessing.dummy import Pool as ThreadPool
from netmiko import ConnectHandler
import credentials # Local import of credentials.py


STARTTIME = datetime.now() # Begin timing the script

config = configparser.ConfigParser()
config.read("netsparkconfig.ini")
OLDCOMM = config.get("snmpinfo", "oldcomm")
ACLNUM = config.get("snmpinfo", "aclnum")
SNMPSERV = config.get("snmpinfo", "snmpserv")
V2CCOMM = config.get("snmpinfo", "v2ccomm")
CONTACT = config.get("snmpinfo", "contact")
LOCATION = config.get("snmpinfo", "location")

USERNAME, PASSWORD, SECRET = credentials.cred_csv()
COMMAND = [ 'no ip access-list standard snmplist',
            'no snmp-server community ' + OLDCOMM,
            'ip access-list standard ' + ACLNUM,
	        'no 10',
	        'no 20',
	        '10 permit host ' + SNMPSERV + ' log',
	        '20 deny any log',
	        'exit',
            'snmp-server community ' + V2CCOMM + ' ro 10',
            'snmp-server contact ' + CONTACT,
            'snmp-server location ' + LOCATION ]

CUSTOMER = input("Which customer? ") + ".csv"
POOL = ThreadPool()


def generate_ip_list(custdictionary):
    '''Return a list of IP's from the dictionary'''
    ip_list = [d['IP_Address'] for d in custdictionary if 'IP_Address' in d]
    return ip_list


def generate_cust_dict(customer):
    '''Generates a dictionary from the customer data csv file'''
    with open(customer, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for line in reader:
            data.append(line)
        return data


def find_by_ip(lst, value):
    '''Returns the row that a specific IP is in (search for row by IP'''
    for row in lst:
        if str(row['IP_Address']) == str(value):
            return row


def generate_switch_dict(username, password, secret, matchrow):
    '''Makes the switch dictionary for Netmiko's connection handler'''
    switch = {
        'device_type': matchrow['device_type'],
        'ip': matchrow['IP_Address'],
        'username': username,
        'password': password,
        'secret': secret,
        'verbose': False,
        }
    return switch


def switch_run_command(ipaddr):
    '''All the logic happens here. Take the data, process it, print results'''
    matchrow = find_by_ip(CUSTDICTIONARY, ipaddr)
    sessiondict = generate_switch_dict(USERNAME, PASSWORD, SECRET, matchrow)
    session = ConnectHandler(**sessiondict)
    session.enable()
    session.send_config_set(COMMAND)
    session_return = session.send_command('show run | in snmp')
    hostname = matchrow['SysName']
    # Fancy formatting here for results
    print("\n\n>>>>>>>>> {0} {1} <<<<<<<<<\n".format(hostname, ipaddr)
          + session_return
          + "\n>>>>>>>>> End <<<<<<<<<\n")
    # Disconnect the netmiko session
    session.disconnect()


CUSTDICTIONARY = generate_cust_dict(CUSTOMER)
IP_LIST = generate_ip_list(CUSTDICTIONARY)

RESULTS = POOL.map(switch_run_command, IP_LIST)

POOL.close()
POOL.join()

ENDTIME = datetime.now()
TOTALTIME = ENDTIME - STARTTIME
print("\nTotal time for script: \n" + str(TOTALTIME))
