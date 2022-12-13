import time
import os
import yaml
from pathlib import Path
import argparse
from functools import partial
from src.classes.action import Action
from src.classes.mailbox import Mailbox
from src.classes.parser import Parser
from src.classes.logger import custom_log


def main(config_file, email_number):
    cfg = yaml.safe_load((Path(config_file).read_text()))

    mailbox = Mailbox(cfg['e_mail'])
    i = 0
    for email_uid, part, email_body in mailbox.read_email():
        if i >= int(email_number):
            break
        parser = Parser(cfg['parser'], part, email_body)
        parse_result = parser.parse()

        if len(parse_result) > 0:
            action = Action(pipeline=cfg['action'], args=parse_result, model=cfg['model'])
            response_code, response_text = action.run()
            if response_code == 0:
                custom_log(f'E-mail successfully processed: {response_text}', 'green')
                #mailbox.move_email(email_uid)
        i = i + 1
    mailbox.disconnect()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="E-mail parser")
    parser.add_argument('-c', dest='config_file', help='yaml config file', required=True)
    parser.add_argument('-n', dest='email_number', help='number of e-mails to be processed', required=True)
    args = parser.parse_args()
    main(args.config_file, args.email_number)
