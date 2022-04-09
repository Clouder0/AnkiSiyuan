from .parser import siyuan as parser
from siyuanhelper import helper as siyuanhelper
from AnkiIn.helper import ankiConnectHelper as ankihelper
from AnkiIn.config import dict as conf
from . import config
from . import config_parser
import datetime
import asyncio
import time


updated_notes = 0
added_notes = 0


async def execute():
    if not ankihelper.check_online():
        print("Anki is not online! Please open Anki and make sure anki-connect is installed.")
        return
    start_time = time.perf_counter()
    config_parser.parse()
    print("Api Token:{}".format(conf["siyuan"]["api_token"]))
    print("Last Sync:{}".format(config.last_sync_time))
    this_sync_time = datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")
    print("Now Sync: {}".format(this_sync_time))
    noteList = await parser.sync(config.last_sync_time)
    for x in noteList:
        if x is None:
            continue
        handle(x)
    print("Added {} notes, updated {} notes.".format(added_notes, updated_notes))
    end_time = time.perf_counter()
    print("Time consumed: {}s".format(end_time - start_time))
    f = open("last_sync_time", "w", encoding="UTF-8")
    f.write(this_sync_time)
    f.close()


def handle(x):
    global updated_notes, added_notes
    old = ankihelper.find_notes("SiyuanID:\"{}\"".format(x.outputfields["SiyuanID"]))
    # print(x.outputfields["SiyuanID"])
    # print(x.SiyuanID)
    if len(old) >= 2:
        print("found SiyuanID[{}] with duplicates in Anki!\n{}".format(
            x["SiyuanID"], old))
    elif len(old) == 1:
        ankihelper.update_note_fields(old[0], x)
        print("updated: SiyuanID[{}] AnkiID[{}]".format(
            x.fields["SiyuanID"], old[0]))
        updated_notes = updated_notes + 1
    else:
        ankihelper.add_note(x)
        added_notes = added_notes + 1


def execute_from_commandline():
    asyncio.run(execute())
