import argparse
import contextlib
import os.path

import toml

from AnkiIn import config as ankiin_config
from AnkiIn.config import dict as conf

from . import config


version_name = '0.1.0'

help_info = {'config': 'set your config file path.'}

parser = argparse.ArgumentParser(
    description='AnkiSiyuan. Link your data in Siyuan with Anki!'
)
parser.add_argument(
    '-v', '--version', action='version', version=f'Anki Siyuan v{version_name}'
)
parser.add_argument(
    '-c',
    '--config',
    metavar='config',
    default=config.config_path,
    help=help_info['config'],
)


def enable_log_file():
    conf['log_config']['handlers']['log_file'] = {
        'level': 'DEBUG' if config.log_debug else 'INFO',
        'formatter': 'standard',
        'class': 'logging.FileHandler',
        'filename': 'log.txt',
        'mode': 'a',
    }
    for x in conf['log_config']['loggers'].keys():
        conf['log_config']['loggers'][x]['handlers'].append('log_file')


def parse():
    args = parser.parse_args()
    config.config_path = args.config
    conf['siyuan'] = {}
    conf['siyuan']['api_token'] = ''
    conf['siyuan']['custom_attr_name'] = 'custom-ankilink'
    conf['siyuan']['assets_replacement'] = 'assets'
    with contextlib.suppress(Exception), open(
        'last_sync_time', 'r', encoding='UTF-8'
    ) as f:
        config.last_sync_time = f.read()
    enable_log_file()
    load_config_file()
    ankiin_config.update_config()


def load_config_file():
    if os.path.isfile(config.config_path):
        ankiin_config.execute_config(toml.load(config.config_path))
    else:
        print(f"Warning: Config File {config.config_path} doesn't exist!")
