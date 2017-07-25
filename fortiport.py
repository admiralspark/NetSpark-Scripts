'''
This script will parse a daily report, called Threats.csv, and spit out relevant information
so that we can save time on risk mitigation in the morning. 
'''

import csv
import socket


REPORTNAME = "Threats.csv"

def getListItemIndex(itemname, listname):
    'This queries listname for itemname, and returns the index of that list containing itemname'
    for list in listname:
        for item in list:
            if item == itemname:
                n1 = listname.index(list)
                n2 = list.index(item)
                return n1, n2

def getMatches(index1, index2):
    'This provides relevant information from the report'
    for i in range(index1, index2):
        if '10.0' in str(fortilist[i]):
            try:
                print(fortilist[i][1] + " --> " + socket.gethostbyaddr(fortilist[i][1]))
            except:
                print(fortilist[i][1])
        if '172.16' in str(fortilist[i]):
            print(fortilist[i][1])
            try:
                print(fortilist[i][1] + " --> " + socket.gethostbyaddr(fortilist[i][1]))
            except:
                print(fortilist[i][1])
        if '.com' in str(fortilist[i]):
            try:
                print(fortilist[i][1] + " --> " + socket.gethostbyname(fortilist[i][1]))
            except:
                print(fortilist[i][1])




with open (REPORTNAME, 'r') as f:
    reader = csv.reader(f)
    fortilist = list(reader)

    intvic = getListItemIndex('###Intrusion Victims###', fortilist)
    intsrc = getListItemIndex('###Intrusion Sources###', fortilist)
    intblk = getListItemIndex('###Intrusions Blocked###', fortilist)

    # VICTIMS
    print('\n--------Intrusion Victims--------\n')
    getMatches(intvic[0], intsrc[0])
    print('\n---------------------------------\n')

    #SOURCES
    print('\n--------Intrusion Sources--------\n')
    getMatches(intsrc[0], intblk[0])
    print('\n---------------------------------\n')
