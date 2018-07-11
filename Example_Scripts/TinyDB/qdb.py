'''
-------------------------------------------------------------------------------
This script is for testing EasyGUI
-------------------------------------------------------------------------------
'''
# Separated namespace
import easygui as g
# Local functions
import dbquery

OPENINGMSG = "What would you like to look up?"
TITLE = "DB Query Application"
CHOICES = ["Department", "IP", "Hostname", "Device Type"]
CHOICE = g.choicebox(OPENINGMSG, TITLE, CHOICES)

if CHOICE == "Department":
    department = g.enterbox("What is the dept you want to search for?", TITLE)
    RDept = dbquery.querydept(department)
    g.msgbox(RDept, TITLE)

elif CHOICE == "IP":
    ip = g.enterbox("What is the ip you want to search for?", TITLE)
    RIP = dbquery.queryip(ip)
    g.msgbox(RIP, TITLE)

elif CHOICE == "Hostname":
    hostname = g.enterbox("What is the hostname you want to search for?", TITLE)
    RHost = dbquery.queryip(hostname)
    g.msgbox(RHost, TITLE)

elif CHOICE == "Device Type":
    device_type = g.enterbox("What is the device type you want to search for?", TITLE)
    RdType = dbquery.queryip(device_type)
    g.msgbox(RdType, TITLE)
    