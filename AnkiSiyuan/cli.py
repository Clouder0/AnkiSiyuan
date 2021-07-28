from AnkiIn.parser import siyuan as parser
from AnkiIn.helper import siyuanHelper as siyuanhelper
from AnkiIn.helper import ankiConnectHelper as ankihelper
import config
import config_parser
import datetime


def execute_from_commandline():
    config_parser.parse()
    print(config.auth_code)
    siyuanhelper.login(config.auth_code)
    print(config.last_sync_time)
    this_sync_time = datetime.datetime.now().strftime(r"%Y%m%d%H%M%S")
    print(this_sync_time)
    noteList = parser.sync(config.last_sync_time)
    updated_notes = 0
    added_notes = 0
    for x in noteList:
        if x is None:
            continue
        # print(x.fields)
        old = ankihelper.find_notes("SiyuanID:\"{}\"".format(x.outputfields["SiyuanID"]))
        # print(x.outputfields["SiyuanID"])
        # print(x.SiyuanID)
        if len(old) >= 2:
            print("Found SiyuanID[{}] with duplicates in Anki!\n{}".format(
                x["SiyuanID"], old))
        elif len(old) == 1:
            ankihelper.update_note_fields(old[0], x)
            print("Anki Note {} updated.".format(old[0]))
            updated_notes = updated_notes + 1
        else:
            ankihelper.add_note(x)
            added_notes = added_notes + 1
    print("added {} notes, updated {} notes.".format(added_notes, updated_notes))
    f = open("last_sync_time", "w", encoding="UTF-8")
    f.write(this_sync_time)
    f.close()


if __name__ == "__main__":
    execute_from_commandline()
