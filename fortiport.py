'''
This script will parse a daily report, called Threats.csv, and spit out relevant information
so that we can save time on risk mitigation in the morning. 
'''

import csv
import socket
import configparser

config = configparser.ConfigParser()
config.read("netsparkconfig.ini")
vulnerabilities = (config.get("fortiport", "vulnerabilities")).split(',')
domaincheck = (config.get("fortiport", "domain_names")).split(',')
REPORTNAME = "Threats.csv"

def getListItemIndex(itemname, listname):
    'This queries listname for itemname, and returns the index of that list containing itemname'
    for list1 in listname:
        for item in list1:
            if item == itemname:
                n1 = listname.index(list1)
                n2 = list1.index(item)
                return n1, n2

def getMatchesIP(index1, index2):
    'This provides relevant information from the report'
    for i in range(index1, index2):
        if '10.0' in str(fortilist[i]):
            try:
                print(fortilist[i][1] + " --> " + socket.gethostbyaddr(fortilist[i][1]))
            except:
                print(fortilist[i][1])
        if '172.16' in str(fortilist[i]):
            try:
                print(fortilist[i][1] + " --> " + socket.gethostbyaddr(fortilist[i][1]))
            except:
                print(fortilist[i][1])
        for k in domaincheck:
            if k in str(fortilist[i]):
                try:
                    print(fortilist[i][1] + " --> " + socket.gethostbyname(fortilist[i][1]))
                except:
                    print(fortilist[i][1])

def getMatchesInfect(ind1, ind2):
    'This provides matches to stuff we care about'
    for i in range(ind1, ind2):
        for j in vulnerabilities:
            if j in str(fortilist[i]).lower():
                print(fortilist[i][1] + " " + fortilist[i][2])



with open (REPORTNAME, 'r') as f:
    reader = csv.reader(f)
    fortilist = list(reader)

    intvic = getListItemIndex('###Intrusion Victims###', fortilist)
    intsrc = getListItemIndex('###Intrusion Sources###', fortilist)
    intblk = getListItemIndex('###Intrusions Blocked###', fortilist)
    inttml = getListItemIndex('###Intrusion Timeline###', fortilist)

    #VICTIMS
    print('\n--------Intrusion Victims--------\n')
    getMatchesIP(intvic[0], intsrc[0])
    print('\n---------------------------------\n')

    #SOURCES
    print('\n--------Intrusion Sources--------\n')
    getMatchesIP(intsrc[0], intblk[0])
    print('\n---------------------------------\n')

    #BLOCKEDLIST
    print('\n--------Intrusions Blocked-------\n')
    getMatchesInfect(intblk[0], inttml[0])
    print('\n---------------------------------\n')
