import json
import os
import shutil

DEFAULT_CONFIG = {
    'VERSION': 0,
    'LANG': 'zh-CN',
    'SERVERS': []
}


class Config:
    def __init__(self):
        self.config = dict

    def initial_config(self):
        # Initialization
        if os.path.exists('nmsl.json'):
            self.initial_empty_config()
        else:
            self.read_config()
            if not self.validate_config():
                shutil.copy('nmsl.json', 'nmsl.json.bak')
                self.initial_empty_config()

    def validate_config(self):
        # Do Validation and Correction
        if 'VERSION' not in self.config:
            return False
        return True

    def initial_empty_config(self):
        self.config = DEFAULT_CONFIG
        self.save_config()

    def read_config(self):
        with open('nmsl.json', 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open('nmsl.json', 'w') as f:
            json.dump(self.config, f)
