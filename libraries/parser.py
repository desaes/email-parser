import re
import libraries.logger
import libraries.util
import email

class Parser:
    def __init__(self, config: dict, msg: email.message.EmailMessage, email_body: str) -> None:
        print(email_body)
        self.config = config
        self.email_as_dict = {
            'From': msg['From'],
            'Subject': msg['Subject'],
            'Body': email_body
        }

    def parse(self) -> list:
        data = []
        for parse_type in self.config:
            if parse_type == 'CaptureText':
                for item in self.config['CaptureText']:
                    for field, search_exp in self.config['CaptureText'][item].items():
                        if search_exp != None:
                            result = re.search(search_exp, self.email_as_dict[item])
                            if result.group(1):
                                data.append(
                                        {
                                            field.split(',')[1]: result.group(1)
                                        }
                                    )
            if parse_type == 'StaticText':
                for field, value in self.config['StaticText'].items():
                    data.append(
                        {
                            field.split(',')[1]: value
                        }
                    )
        return(data)
                            


                    

