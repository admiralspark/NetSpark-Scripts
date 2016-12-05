'''
This script logs in to switches, checks the existing local usernames against
the allowed list, and remediates them if inconsistencies are found.
'''

#Global imports
from netmiko import ConnectHandler
from datetime import datetime
import csv, os.path
#Local imports
import credentials

# Begin timing Script
start_time = datetime.now()
