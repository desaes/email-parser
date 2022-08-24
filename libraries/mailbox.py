import imaplib
import email
import chardet
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
    def __init__(self, id: int, config) -> None:
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

    def read_email(self, move=False) -> None:
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
            msgs = email.message_from_string(data[0][1].decode('utf-8'))
            #custom_log(msgs, 'blue')
            for msg in unpack_email(msgs):
                libraries.logger.custom_log(f'Content_type: {msg.get_content_maintype()}', 'cyan')
                if msg.get_content_maintype() == 'multipart':
                        continue                
                for k, v in msg.items():
                    libraries.logger.custom_log(f'======> Key: {k}', 'red')
                    libraries.logger.custom_log(f'======> Value: {v}', 'yellow')

                if msg.get_content_maintype() == 'text':
                    libraries.logger.custom_log(f'======> Body:', 'green')
                    data = libraries.util.decode_str(msg.get_payload())
                    print(data)

