import imaplib
import base64
import os
import email
import configparser
config = configparser.ConfigParser()

config.read('C:\Dev\l-python\email\config.ini')

imap_host = config.get("mail", "imap_host")
imap_user = config.get("mail", "imap_user")
imap_pass = config.get("mail", "imap_pass")
path = 'c:/temp'
 
# For this example, our host will be gmail
mailbox = imaplib.IMAP4(imap_host)
mailbox.login(imap_user, imap_pass)
mailbox.select('Inbox')
 
type, data = mailbox.search(None, 'ALL')
mail_ids = data[0]
id_list = mail_ids.split()
 
for num in data[0].split():
    typ, data = mailbox.fetch(num, '(RFC822)' )
    raw_email = data[0][1]
 
# Converting bytes into string format
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
 
# Iteration to downlaod the attachments
    for part in email_message.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()
        if bool(fileName):
            filePath = os.path.join(path, fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
 
# Closing the session and logging out
mailbox.close()
mailbox.logout()