import daemon
import time
import os
from concurrent import futures
import multiprocessing
import itertools
import json
from functools import partial
import pprint

from libraries.config import Config
from libraries.mailbox import Mailbox
from libraries.parser import Parser

PROCS_BY_CORE = 2

def validate_yaml_structure():
    pass


#def parse(a: str, b: str):
def parse(mailbox: Mailbox, config):
    with open('/tmp/log.txt', 'a') as fd:
        fd.write(f"mailbox: {mailbox.id}\n")
        fd.write(f"config: {config}\n")        

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
                result = parser.parse()
                if len(result) > 0:
                    print(result)


        
        
        #time.sleep(1)

#with daemon.DaemonContext():
if __name__ == '__main__':
    main()