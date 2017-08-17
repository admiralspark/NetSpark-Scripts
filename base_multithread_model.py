'''
-------------------------------------------------------------------------------
This script is a baseline for multithreaded conversion of all of the scripts.
I'll look into converting the repo to use multithread, some day.
-------------------------------------------------------------------------------
'''

from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool
import credentials # Local import of credentials.py


start_time = datetime.now() # Begin timing the script

CUSTOMER = input("Which file? ") + ".csv"
USERNAME, PASSWORD, SECRET = credentials.cred_csv()
COMMAND = input("What command do you want to run? ")
pool = ThreadPool()


def generate_ip_list(CUSTDICTIONARY):
    ip_list = [d['IP_Address'] for d in CUSTDICTIONARY if 'IP_Address' in d]
    return ip_list


def generate_cust_dict(CUSTOMER):
    with open(CUSTOMER, mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for line in reader:
            data.append(line)
        return data


def find_by_ip(lst, value):
    for row in lst:
        if str(row['IP_Address']) == str(value):
            return row


def generate_switch_dict(username, password, secret, matchrow):
    switch = {
                'device_type': matchrow['device_type'],
                'ip': matchrow['IP_Address'],
                'username': username,
                'password': password,
                'secret': secret,
                'verbose': False,
            }
    return switch


def switch_run_command(ip):
    matchrow = find_by_ip(CUSTDICTIONARY, ip)
    sessionDict = generate_switch_dict(USERNAME, PASSWORD, SECRET, matchrow)
    session = ConnectHandler(**sessionDict)
    session.enable()
    session_return = session.send_command(COMMAND)
    hostname = matchrow['SysName']
    # Fancy formatting here for results
    print("\n\n>>>>>>>>> {0} {1} <<<<<<<<<\n".format(hostname, ip)
          + session_return
          + "\n>>>>>>>>> End <<<<<<<<<\n")
    # Disconnect the netmiko session
    session.disconnect()


CUSTDICTIONARY = generate_cust_dict(CUSTOMER)
IP_LIST = generate_ip_list(CUSTDICTIONARY)

results = pool.map(switch_run_command, IP_LIST)

pool.close()
pool.join()

end_time = datetime.now()
total_time = end_time - start_time
print("\nTotal time for script: \n" + str(total_time))