from .SCloze import get as cget
from AnkiIn.notetypes.ListCloze import check as super_check
from AnkiIn.config import dict as conf
from AnkiIn.config import config_updater


notetype_name = "SListCloze"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_siyuan_list_cloze_config():
    global settings, priority

    priority = settings.get("priority", 16)


config_updater.append((update_siyuan_list_cloze_config, 16))


def check(lines: list, extra_params={}) -> bool:
    return super_check(lines=lines, extra_params=extra_params)


def get(text: str, deck: str, tags: list, extra_params={}):
    return cget(text=text, deck=deck, tags=tags, extra_params=extra_params)
