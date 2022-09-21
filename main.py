import time
import os
from functools import partial
from src.classes.action import Action
from src.classes.mailbox import Mailbox
from src.classes.parser import Parser
from src.classes.logger import custom_log
import hydra

@hydra.main(config_path="conf", version_base=None)
def main(cfg):

    mailbox = Mailbox(cfg.e_mail)
    for email_uid, part, email_body in mailbox.read_email():
        parser = Parser(cfg.parser, part, email_body)
        parse_result = parser.parse()
        if len(parse_result) > 0:
            action = Action(pipeline=cfg.action, args=parse_result, model=cfg.model)
            response_code, response_text = action.run()
            if response_code == 0:
                custom_log(f'E-mail successfully processed: {response_text}', 'green')
                mailbox.move_email(email_uid)
            break
    mailbox.disconnect()

if __name__ == '__main__':
    main()