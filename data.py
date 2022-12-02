import json
import os
import shutil

DEFAULT_NMSL_CONFIG = {
    'VERSION': 0,
    'LANG': 'zh-CN',
    'SERVERS': {}
}

DEFAULT_SERVER_CONFIG = {
    'CONFIG_VERSION': DEFAULT_NMSL_CONFIG['VERSION'],
    'VERSION': 'Unknown',
    'NAME': 'Untitled',
    'SERVERSIDE': 'Vanilla',
    'EXEC_TYPE': 'java',
    'EXEC': '-jar server.jar'
}


class NMSLConfig:
    def __init__(self):
        self.config = []
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
            self.config['SERVERS'] = {}
            self.save_config()
        if type(self.config['SERVERS']) == list:
            r = {}
            for _ in self.config['SERVERS']:
                sc = ServerConfig(_)
                r[sc.config['NAME']] = _
            self.config['SERVERS'] = r
            self.save_config()
        return self.config['SERVERS'].keys()

    def add_server(self, sc):
        self.config['SERVERS'][sc.config['NAME']] = sc.path
        self.save_config()


class ServerConfig:
    def __init__(self, path):
        self.path = path
        self.config = []
        self.initial_config()

    @property
    def config_path(self):
        return f'{self.path}/server.nmsl.json'

    def initial_config(self):
        # Initialization
        if os.path.exists(self.config_path):
            self.read_config()
            shutil.copy(self.config_path, f'{self.config_path}.bak')
            if not self.validate_config():
                self.initial_empty_config()
        else:
            self.initial_empty_config()

    def initial_empty_config(self):
        self.config = DEFAULT_SERVER_CONFIG.copy()
        self.save_config()

    def validate_config(self):
        if 'NAME' not in self.config:
            self.config['NAME'] = 'Untitled'
        if 'VERSION' not in self.config:
            self.config['VERSION'] = 'Unknown'
        if 'SERVERSIDE' not in self.config:
            self.config['SERVERSIDE'] = 'Vanilla'
        if 'EXEC_TYPE' not in self.config:
            if 'EXEC' in self.config:
                self.config['EXEC_TYPE'] = 'Shell'
            else:
                self.config['EXEC_TYPE'] = 'Java'
                self.config['EXEC'] = '-jar server.jar'
        if 'CONFIG_VERSION' not in self.config:
            return False
        self.save_config()
        return True

    def read_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)
