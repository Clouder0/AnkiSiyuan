from AnkiIn.note import Note
from AnkiIn.config import dict as conf
from AnkiIn.config import config_updater
from AnkiIn.log import notetype_logger as log
from .SQA import SQANote
from AnkiIn.notetypes.MQA import get as super_get
from AnkiIn.notetypes.MQA import check as super_check


notetype_name = "SMQA"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None
prefix = None


def update_siyuan_mqa_config():
    global settings, priority, prefix

    priority = settings.get("priority", 13)
    prefix = settings.get("prefix", "!")


config_updater.append((update_siyuan_mqa_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return super_check(lines=lines, extra_params=extra_params)


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    return SQANote(extra_params["SiyuanID"], super_get(text=text, deck=deck, tags=tags, extra_params=extra_params))
