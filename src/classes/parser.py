import re
import src.classes.logger
import src.libs.util
import email

class Parser:
    def __init__(self, config: dict, msg: email.message.EmailMessage, email_body: str) -> None:
        self.config = config
        self.email_as_dict = {
            'from': msg['from'],
            'subject': msg['subject'],
            'body': email_body
        }

    def parse(self) -> list:
        data = {}
        for parse_type in self.config:
            if parse_type == 'capture_text':
                for item in self.config['capture_text']:
                    for field, search_exp in self.config['capture_text'][item].items():
                        if search_exp != None:
                            result = re.search(search_exp, self.email_as_dict[item])
                            if result:
                                if result.group(1):
                                    data[field.split(',')[1]] = result.group(1)

            if parse_type == 'static_text':
                for field, value in self.config['static_text'].items():
                    data[field.split(',')[1]] = value
        return(data)

