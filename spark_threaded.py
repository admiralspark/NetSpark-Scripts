'''
-------------------------------------------------------------------------------
This script is a baseline for multithreaded conversion of all of the scripts.
I'll look into converting the repo to use multithread, some day.
-------------------------------------------------------------------------------
'''

from datetime import datetime
import csv
from multiprocessing.dummy import Pool as ThreadPool
#from multiprocessing.dummy import cpu_count # Broken as of March 2017 in 3.x
from netmiko import ConnectHandler
import credentials # Local import of credentials.py


STARTTIME = datetime.now() # Begin timing the script

CUSTOMER = "test.csv"
COMMANDLIST = []
command = "sh run"
#POOL = ThreadPool(cpu_count() - 1) # Missing from lib as of 03/2017
POOL = ThreadPool()

def check_config_mode(config):
    '''Verifies if script is running config changes or not'''
    if config is not None:
        return True
    else:
        return False

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


def generate_switch_dict(username, password, secret, matchrow, command):
    '''Makes the switch dictionary for Netmiko's connection handler'''
    swlist = [username, password, secret, matchrow['device_type'], matchrow['IP_Address'], matchrow['SysName'], command]
    return swlist


def generate_listof_lists(custdictionary, command):
    '''Returns a list of lists from the input dictionary'''
    swlist = []
    username, password, secret = credentials.cred_csv()
    for row in custdictionary:
        swlist.append(generate_switch_dict(username, password, secret, row, command))
    return swlist


def switch_run_command(username, password, secret, devicetype, ipaddr, hostname, clicomm):
    '''All the logic happens here. Take the data, process it, print results'''
    sessiondict = {
        'device_type': devicetype,
        'ip': ipaddr,
        'username': username,
        'password': password,
        'secret': secret,
        'verbose': False
        }
    session = ConnectHandler(**sessiondict)
    session.enable()
    session_return = session.send_command(clicomm)
    # Fancy formatting here for results
    print("\n\n>>>>>>>>> {0} {1} <<<<<<<<<\n".format(hostname, ipaddr)
          + session_return
          + "\n>>>>>>>>> End <<<<<<<<<\n")
    # Disconnect the netmiko session
    session.disconnect()


def info_command(command, csv, db, ip, creds):
    '''This runs a single command against all devices'''
    if csv is not None:
        switchdata = generate_cust_dict(csv) #dictionary of all switch data
        switchlists = generate_listof_lists(switchdata, command)
        results = POOL.starmap(switch_run_command, switchlists)
        POOL.close()
        POOL.join()
    elif db is not None:
        print("SQL functionality is not supported at this time.")
        pass
    elif ip is not None:
        pass
    

def config_command(config, csv, db, ip, creds):
    pass


#RESULTS = POOL.map(switch_run_command, IP_LIST)

#POOL.close()
#POOL.join()

ENDTIME = datetime.now()
TOTALTIME = ENDTIME - STARTTIME
