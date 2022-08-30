import daemon
import time
import os
from concurrent import futures
import multiprocessing
import itertools
import json
from functools import partial
import pprint
from libraries.action import Action

from libraries.config import Config
from libraries.mailbox import Mailbox
from libraries.parser import Parser

PROCS_BY_CORE = 2

def validate_yaml_structure():
    pass

def main():
    #while True:
        config = Config(os.getcwd() + '/configs/')
        config_data = config.get_config()
       
        for mailbox in (
            Mailbox(id=item[0], config=item[1]) 
            for item in config_data['mailbox'].items() 
            if item[1]['Mailbox']['Enabled']
            ):
            for email_id, part, email_body in mailbox.read_email():
                parser = Parser(config_data['parser'][mailbox.id], part, email_body)
                parse_result = parser.parse()
                if len(parse_result) > 0:
                    
                    action = Action(mailbox.id, parse_result)
                    action.run()


        
        
        #time.sleep(1)

#with daemon.DaemonContext():
if __name__ == '__main__':
    main()