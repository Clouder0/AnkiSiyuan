import asyncio
import datetime
import time

from AnkiIn.config import dict as conf
from AnkiIn.helper import ankiConnectHelper as ankiHelper

from . import config, config_parser
from .parser import siyuan as parser


updated_notes = 0
added_notes = 0


async def execute():
    if not ankiHelper.check_online():
        print(
            "Anki is not online! Please open Anki and \
make sure anki-connect is installed."
        )
        return
    start_time = time.perf_counter()
    config_parser.parse()
    print(f'Api Token:{conf["siyuan"]["api_token"]}')
    print(f"Last Sync:{config.last_sync_time}")
    this_sync_time = datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")
    print(f"Now Sync: {this_sync_time}")
    note_list = await parser.sync(config.last_sync_time)
    for x in note_list:
        if x is None:
            continue
        handle(x)
    print(f"Added {added_notes} notes, updated {updated_notes} notes.")
    end_time = time.perf_counter()
    print(f"Time consumed: {end_time - start_time}s")
    with open("last_sync_time", "w", encoding="UTF-8") as f:
        f.write(this_sync_time)
        f.close()


def handle(x):
    global updated_notes, added_notes
    old = ankiHelper.find_notes(f"SiyuanID:{x['SiyuanID']}*")
    # print(x.outputfields['SiyuanID'])
    # print(x.SiyuanID)
    if len(old) >= 2:
        print(
            f'found SiyuanID[{x["SiyuanID"]}] with \
            duplicates in Anki!\n{old}'
        )
    elif len(old) == 1:
        ankiHelper.update_note_fields(old[0], x)
        print(f'updated: SiyuanID[{x["SiyuanID"]}] AnkiID[{old[0]}]')
        updated_notes = updated_notes + 1
    else:
        ankiHelper.add_note(x)
        added_notes = added_notes + 1


def execute_from_commandline():
    asyncio.run(execute())
