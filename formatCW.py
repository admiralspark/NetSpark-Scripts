import pyperclip
import smtplib

upd8 = pyperclip.paste()

# Optional, or just set the variable here
servername = "accorp-exch2.accorp.local"
serverport = 25

ticketnum = raw_input("Enter the ticket number: ")
body = "!!AddInternal:" + upd8 + "!!"
fromadd = "Kris@alasconnect.com"
toadd = "helpdesk@alasconnect.com"


server = smtplib.SMTP(servername, serverport)
msg = """From: Kris@alasconnect.com
To: helpdesk@alasconnect.com
Subject: Ticket#{0}

""".format(ticketnum) + body

#print msg
# Send it

server = smtplib.SMTP(servername)
server.sendmail(fromadd, toadd, msg)
server.quit()

print("\nSent the following to Ticket#{0}: \n").format(ticketnum) + msg
