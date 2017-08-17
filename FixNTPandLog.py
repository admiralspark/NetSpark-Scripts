'''
-------------------------------------------------------------------------------
This script is a baseline for multithreaded conversion of all of the scripts.
I'll look into converting the repo to use multithread, some day.
-------------------------------------------------------------------------------
'''

from datetime import datetime
import csv
from multiprocessing.dummy import Pool as ThreadPool
from netmiko import ConnectHandler
import configparser
import credentials # Local import of credentials.py


STARTTIME = datetime.now() # Begin timing the script

config = configparser.ConfigParser()
config.read("netsparkconfig.ini")
NTPSERVER = "ntp server " + config.get("companystd", "ntp_server")
OLDNTPSERVER = "no ntp server " + config.get("companystd", "old_ntp_server")
TIMEZONE = "clock summer-time " + config.get("companystd", "timezone") + " recurring"
LOGSERVER = "logging host " + config.get("companystd", "log_server") + " transport udp port " + config.get("companystd", "logsrv_port")

CUSTOMER = input("Which file? ") + ".csv"
USERNAME, PASSWORD, SECRET = credentials.cred_csv()
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
    hostname = matchrow['SysName']
    # ----------NTP-------------
    ntp_settings = [OLDNTPSERVER,
                    NTPSERVER,
                    'no clock summer-time',
                    TIMEZONE,
                    'service timestamps log datetime localtime show-timezone',
                    'service timestamps debug datetime localtime show-timezone']

    session.send_config_set(ntp_settings)
    #----------logging-----------
    log_settings = ['logging trap notifications',
                    'logging facility syslog',
                    LOGSERVER]
    session.send_config_set(log_settings)
    #-----------------------------
    resultsntp = session.send_command("sh run | in ntp|timezone|clock")
    resultslog = session.send_command("sh run | in logging")
    # Fancy formatting here for results
    print("\n\n>>>>>>>>> {0} {1} <<<<<<<<<\n".format(hostname, ipaddr)
          + resultsntp
          + "\n\n"
          + resultslog
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
