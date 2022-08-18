import imaplib, email
from email.header import Header
from email.header import decode_header
from email.utils import parseaddr, formataddr
import logging
import pprint
import configparser
config = configparser.ConfigParser()
config.read('C:\Dev\l-python\email\config.ini')

imap_host = config.get("mail", "imap_host")
imap_user = config.get("mail", "imap_user")
imap_pass = config.get("mail", "imap_pass")

print(imap_host, imap_user, imap_pass)

with imaplib.IMAP4(imap_host, 143) as imap:
    imap.login(imap_user, imap_pass)

    tmp, data = imap.list()
    print(data)

    imap.select('Inbox')

    tmp, data = imap.search(None, 'ALL')
    for num in data[0].split():
        tmp, data = imap.fetch(num, 'RFC822')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        print(email.message_from_string(raw_email_string))
        #tmp, data = imap.fetch(num, '(RFC822)')
        #tmp, data = imap.fetch(num, '(BODY.PEEK[HEADER] FLAGS)')
        
        #print('Message: {0}\n'.format(num))
        #pprint.pprint(data[0][1])
        #pprint.pprint(data)
#        break
