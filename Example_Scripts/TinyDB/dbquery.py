"""
-------------------------------------------------------------------------------
This script just queries the database as a test for me. It can be used as an
example of how TinyDB queries can be done.
I'm just sick of typing it in the interpreter over and over.
-------------------------------------------------------------------------------
"""
from tinydb import TinyDB, Query

# Define the Database
DB = TinyDB('netspark.json')

def querydept(department):
    Device = Query()
    dblineD = DB.search(Device.department == department)
    return dblineD

def queryip(ip):
    Device = Query()
    dblineI = DB.search(Device.ip == ip)
    return dblineI

def queryhost(hostname):
    Device = Query()
    dblineH = DB.search(Device.hostname == hostname)
    return dblineH

def querytype(device_type):
    Device = Query()
    dblineT = DB.search(Device.device_type == device_type)
    return dblineT