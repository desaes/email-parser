import os
from libraries.config import Config

config = Config(os.getcwd() + '/configs/')
print(config.get_config())