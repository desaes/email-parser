import imaplib
import email
import email.policy
import html2text
import src.classes.logger
import src.libs.util
from src.libs.util import filter_builder
import re
import os


class Mailbox:
    
    def __init__(self, config:dict) -> None:
        self.config = config
        self.__auth = False
        self.imap = imaplib.IMAP4(self.config['mail_box']['imap_host'])
        self.filter =  filter_builder(config['filters'])
        self.auth(config['mail_box'])
        if self.__auth:
            self.imap.create('processed')
    
    def __bool__(self):
        return self.__auth

    def auth(self, params) -> None:
            
            src.classes.logger.custom_log(f"Trying to authenticate: {os.getenv('IMAP_USERNAME')}", 'yellow')
            """
            result, _ = self.imap.login(self.config['mail_box']['imap_user'], self.config['mail_box']['imap_pass'])
            src.classes.logger.custom_log(f"Trying to authenticate: {os.getenv('IMAP_USER')}", 'yellow')
            """
            result, _ = self.imap.login(os.getenv('IMAP_USERNAME'), os.getenv('IMAP_PASSWORD'))
            if result != 'OK':
                raise Exception(f"Error connecting to mail_box: {os.getenv('IMAP_USERNAME')}")
            else:
                src.classes.logger.custom_log(f"Successfully autheticated: {os.getenv('IMAP_USERNAME')}", 'green')
                self.__auth = True

    def disconnect(self) -> None:
        if self:
            self.imap.logout()

    def move_email(self, id: int) -> None:
        result = self.imap.uid('MOVE', str(id).encode(), 'processed')
        if result[0] != 'OK':
            raise Exception(f"Error moving e-mail to processed folder")

    def read_email(self, move=False) -> str:
        result, data = self.imap.select(self.config['mail_box']['imap_input_mbox'])
        if result != 'OK':
            raise Exception(f"Error opening folder {self.config['mail_box']['imap_input_mbox']}")
        if data == ['0']:
            return None
        result, data = self.imap.search(None, self.filter)
        if result != 'OK':
            raise Exception(f"Error when searching for messages using filter: {self.filter}")
        for num in data[0].split():
            try:
                result, uid = self.imap.fetch(num, '(UID)')
            except Exception as e:
                raise Exception(f"Error when fetching message by UID: {num} - {e}")
            if result != 'OK':
                raise Exception(f"Error reading message: {num}")
            uid = int(re.search(r'\(UID\s+(\d+)+\)', uid[0].decode()).group(1))
            result, data = self.imap.fetch(num, '(RFC822)')
            if result != 'OK':
                raise Exception(f"Error reading message: {num}")
            msgs = email.message_from_bytes(data[0][1], policy=email.policy.default)
            #libraries.logger.custom_log(type(msgs), 'blue')
            #for msg in unpack_email(msgs):
            for part in msgs.walk():
                #libraries.logger.custom_log(f'Content_type: {part.get_content_maintype()}', 'cyan')
                if part.get_content_maintype() == 'multipart':
                    continue
                #for k, v in msgs.items():
                    #libraries.logger.custom_log(f'======> Key: {k}', 'red')
                    #libraries.logger.custom_log(f'======> Value: {v}', 'yellow')
                if part.get_content_maintype() == 'text':
                    charset = part.get_content_charset()
                    content_type = part.get_content_type()
                    if content_type == "text/plain" or content_type == "text/html":
                        msg_payload = part.get_payload(decode=True)
                        if msg_payload:
                            if charset:
                                if content_type == "text/plain":
                                    yield uid, msgs, msg_payload.decode(charset)
                                elif content_type == "text/html":
                                    yield uid, msgs, html2text.html2text(msg_payload.decode(charset))
                            else:
                                try:
                                    if content_type == "text/plain":
                                        yield uid, msgs, msg_payload.decode()
                                    elif content_type == "text/html":
                                        yield uid, msgs, html2text.html2text(msg_payload.decode(charset))
                                except Exception as e:
                                    src.classes.logger.custom_log(f"Error trying to decode message using utf-8: {e}", 'red')
                                    src.classes.logger.custom_log(f"Trying to decode message using iso8859-1", 'yellow')
                                    try:
                                        if content_type == "text/plain":
                                            yield uid, msgs, msg_payload.decode("iso8859-1")
                                        elif content_type == "text/html":
                                            yield uid, msgs, html2text.html2text(msg_payload.decode("iso8859-1"))
                                    except Exception as e:
                                        src.classes.logger.custom_log(f"Error trying to decode message using iso8859-1: {e}", 'red')
                                        if content_type == "text/plain":
                                            yield uid, msgs, msg_payload
                                        elif content_type == "text/html":
                                            yield uid, msgs, html2text.html2text(msg_payload)



