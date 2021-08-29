from AnkiIn.parser import siyuan as parser
from AnkiIn.helper import siyuanHelper as siyuanhelper
from AnkiIn.helper import ankiConnectHelper as ankihelper
from . import config
from . import config_parser
import datetime
import aiohttp
import asyncio
import time


updated_notes = 0
added_notes = 0


async def execute():
    start_time = time.perf_counter()
    session = aiohttp.ClientSession()
    siyuanhelper.set_session(session)
    config_parser.parse()
    print(config.auth_code)
    print(config.last_sync_time)
    this_sync_time = datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")
    print(this_sync_time)
    noteList = await parser.sync(config.last_sync_time)
    for x in noteList:
        if x is None:
            continue
        handle(x)
    print("added {} notes, updated {} notes.".format(added_notes, updated_notes))
    end_time = time.perf_counter()
    print("Time consumed: {}s".format(end_time - start_time))
    f = open("last_sync_time", "w", encoding="UTF-8")
    f.write(this_sync_time)
    f.close()
    await session.close()


def handle(x):
    global updated_notes, added_notes
    old = ankihelper.find_notes("SiyuanID:\"{}\"".format(x.outputfields["SiyuanID"]))
    # print(x.outputfields["SiyuanID"])
    # print(x.SiyuanID)
    if len(old) >= 2:
        print("Found SiyuanID[{}] with duplicates in Anki!\n{}".format(
            x["SiyuanID"], old))
    elif len(old) == 1:
        ankihelper.update_note_fields(old[0], x)
        print("Updated: SiyuanID[{}] AnkiID[{}]".format(
            x.fields["SiyuanID"], old[0]))
        updated_notes = updated_notes + 1
    else:
        ankihelper.add_note(x)
        added_notes = added_notes + 1


def execute_from_commandline():
    asyncio.run(execute())
