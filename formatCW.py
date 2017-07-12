import pyperclip
import smtplib

upd8 = pyperclip.paste()

# Optional, or just set the variable here
servername = "emailserver.contoso.com"
serverport = 25

ticketnum = raw_input("Enter the ticket number: ")
body = "!!AddInternal:" + upd8 + "!!"
fromadd = "JohnUser@contoso.com"
toadd = "CWpilot@contoso.com"


server = smtplib.SMTP(servername, serverport)
msg = """From: JohnUser@contoso.com
To: CWpilot@contoso.com
Subject: Ticket#{0}

""".format(ticketnum) + body

#print msg
# Send it

server = smtplib.SMTP(servername)
server.sendmail(fromadd, toadd, msg)
server.quit()

print("\nSent the following to Ticket#{0}: \n").format(ticketnum) + msg
