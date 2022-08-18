import imaplib, base64, email
import pprint
import configparser
config = configparser.ConfigParser()
config.read('C:\Dev\l-python\email\config.ini')

imap_host = config.get("mail", "imap_host")
imap_user = config.get("mail", "imap_user")
imap_pass = config.get("mail", "imap_pass")
 

# connecting to host via SSL
imap = imaplib.IMAP4_SSL(imap_host)
 
# logging in to servers
imap.login(imap_user, imap_pass)
 
# Selecting the inbox of the logged in account
imap.select('Inbox')
 
 
tmp, data = imap.search(None, 'ALL')
for num in data[0].split():
    tmp, data = imap.fetch(num, '(RFC822)')
    print('Message: {0}\n'.format(num))
    pprint.pprint(data[0][1])
    break
imap.close()