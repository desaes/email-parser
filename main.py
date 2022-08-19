import os
from libraries.config import Config

mbox_config = Config(os.getcwd() + '/configs/mailbox')
global_config = Config(os.getcwd() + '/configs/global')
print(global_config.get_config())