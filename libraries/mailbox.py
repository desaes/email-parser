import imaplib
import email
import email.policy
from logging.config import dictConfig
import libraries.logger
import libraries.util

def filter_builder(params):
    """
    Build a text filter based on configuration filter
    """
    filter = ""
    for key, value in params.items():
        if value:
            filter += f"{key.upper()} \"{value}\" "
    
    if filter:
        return f"({filter.rstrip()})"
    else:
        return "(ALL)"

def unpack_email(msgs):
    """
    Create a list with the message or messages (multipart)
    """
    result = []
    if msgs.is_multipart():
        result.append(msgs)
        for msg in msgs.get_payload():
            #if isinstance(msg, (list, tuple)):
            if hasattr(msg, "__iter__") and not isinstance(msg, str):
                result.extend(unpack_email(msg))
            else:
                result.append(msg)
    else:
        result.append(msgs)
    return result        

class Mailbox:
    def __init__(self, id: int, config:dict) -> None:
        self.id = id
        self.config = config
        self.imap = imaplib.IMAP4(self.config['Mailbox']['ImapHost'])
        self.filter = filter_builder(config['Filters'])
        self.auth(config['Mailbox'])

    def auth(self, params) -> None:
            libraries.logger.custom_log(f"Trying to authenticate: {self.config['Mailbox']['ImapUser']}", 'yellow')
            result, _ = self.imap.login(self.config['Mailbox']['ImapUser'], self.config['Mailbox']['ImapPass'])
            if result != 'OK':
                raise Exception(f"Error connecting to mailbox: {self.config['Mailbox']['ImapUser']}")
            else:
                libraries.logger.custom_log(f"Successfully autheticated: {self.config['Mailbox']['ImapUser']}", 'green')

    def move_email(self, id: int) -> None:
        pass

    def read_email(self, move=False) -> str:
        result, data = self.imap.select(self.config['Mailbox']['ImapInputMbox'])
        if result != 'OK':
            raise Exception(f"Error opening folder {self.config['Mailbox']['ImapInputMbox']}")
        if data == ['0']:
            return None
        result, data = self.imap.search(None, self.filter)
        if result != 'OK':
            raise Exception(f"Error when searching for messages using filter: {self.filter}")
        for num in data[0].split():
            libraries.logger.custom_log(f"======> Key: {num}", "magenta")
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
                    if part.get_content_type() == "text/plain":
                        msg_payload = part.get_payload(decode=True)
                        if msg_payload:
                            if charset:
                                yield num.decode(), msgs, msg_payload.decode(charset)
                            else:
                                yield num.decode(), msgs, msg_payload.decode()


