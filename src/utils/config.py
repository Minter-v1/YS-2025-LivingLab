import configparser
import os
from pathlib import Path
from shutil import copyfile

class Config:
    def __init__(self,config_path = "../../config/config.ini"):
        self.config = configparser.ConfigParser()
        self.config_path = config_path
        self.load_config()
        
    
    # config.ini 로드
    def load_config(self):
        if not os.path.exists(self.config_path):
            self.create_config()
    
    # config.ini 생성
    def create_config(self):
        template_path = Path("../../config/config.ini.template")
        destination = Path("../../config/config.ini")
        copyfile(template_path, destination)
        return