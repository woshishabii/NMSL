import json
import os
import shutil

DEFAULT_NMSL_CONFIG = {
    'VERSION': 0,
    'LANG': 'zh-CN',
    'SERVERS': []
}

DEFAULT_SERVER_CONFIG = {
    'CONFIG_VERSION': DEFAULT_NMSL_CONFIG['VERSION'],
    'NAME': 'Untitled',
    'VERSION': 'Unknown',
    'SERVERSIDE': 'Vanilla'
}


class NMSLConfig:
    def __init__(self):
        self.config = dict
        self.initial_config()

    def initial_config(self):
        # Initialization
        if not os.path.exists('nmsl.json'):
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
        if 'LANG' not in self.config:
            self.config['LANG'] = 'zh-CN'
            self.save_config()
        return True

    def initial_empty_config(self):
        self.config = DEFAULT_NMSL_CONFIG
        self.save_config()

    def read_config(self):
        with open('nmsl.json', 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open('nmsl.json', 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_servers(self):
        self.read_config()
        if 'SERVERS' not in self.config:
            self.config['SERVERS'] = []
            self.save_config()
        return self.config['SERVERS']


class ServerConfig:
    pass
