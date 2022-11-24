import json
import os


DEFAULT_CONFIG = {
    'VERSION': 0,
    'LANG': 'zh-CN',
    'servers': []
}


def initial_config():
    if os.path.exists('nmsl.json'):
        with open('nmsl.json', 'w') as f:
            json.dump(DEFAULT_CONFIG, f)
