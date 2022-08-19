from hydra import compose, initialize
import glob
import os

class Config:
    def __init__(self, config_path: str) -> None:
        self.__config: dict = {}
        self.__config_path = config_path
        self.read_files(self.__config_path)

    def read_files(self,config_path: str) -> None:
        for filename in glob.iglob(config_path + '**/*.yaml', recursive=True):
            (type, object) = (filename.split('/')[-2],filename.split('/')[-1].split('.')[0])
            with initialize(version_base=None, config_path=f"../{filename.split('/')[-3]}/{filename.split('/')[-2]}"):
                if not type in self.__config:
                    self.__config[type] = {} 
                if not object in self.__config[type]:
                    self.__config[type][object] = compose(config_name=object)
    
    def get_config(self) -> dict:
        return self.__config