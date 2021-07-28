import argparse
import os.path
from AnkiIn.config import dict as conf
from AnkiIn import config as AnkiIn_config
import config
import toml

version_name = "0.0.1"

help_info = {
    "deckname": "Default deck to put your notes on. (default \"Export\")",
    "tags": "Default tags to append to your notes. (default [\"#Export\"])",
    "debug": "Enable this to be in debug mode.",
    "config": "The path of the config file",
    "password": "Your authCode in Siyuan"
}

parser = argparse.ArgumentParser(
    description="AnkiSiyuan. Link your data in Siyuan with Anki!")
parser.add_argument("-v", "--version", action="version",
                    version="Anki Importer v{}".format(version_name))
parser.add_argument("-d", "--deckname", metavar="deckname", default=conf["deck_name"],
                    help=help_info["deckname"])
parser.add_argument("-c", "--config", metavar="config", default=config.config_path,
                    help=help_info["config"])
parser.add_argument("-t", "--tags", metavar="tags", nargs="*", default=conf["tags"],
                    help=help_info["tags"])
parser.add_argument("--debug", action="store_true", default=config.log_debug,
                    help=help_info["debug"])
parser.add_argument("-p", "--password", metavar="password", default="",
                    help=help_info["password"])


def enable_log_file():
    conf["log_config"]["handlers"]["log_file"] = {
        "level": "DEBUG" if config.log_debug else "INFO",
        "formatter": "standard",
        "class": "logging.FileHandler",
        "filename": "log.txt",
        "mode": "a"
    }
    for x in conf["log_config"]["loggers"].keys():
        conf["log_config"]["loggers"][x]["handlers"].append("log_file")


def parse():
    args = parser.parse_args()
    conf["deck_name"] = args.deckname
    conf["tags"] = args.tags
    config.log_debug = args.debug
    config.config_path = args.config
    config.auth_code = args.password
    try:
        f = open("last_sync_time", "r", encoding="UTF-8")
        config.last_sync_time = f.read()
        f.close()
    except Exception:
        pass
    enable_log_file()
    load_config_file()
    AnkiIn_config.update_config()


def load_config_file():
    if os.path.isfile(config.config_path):
        AnkiIn_config.execute_config(toml.load(config.config_path))
    else:
        print("Warning: Config File {} doesn't exist!".format(config.config_path))
