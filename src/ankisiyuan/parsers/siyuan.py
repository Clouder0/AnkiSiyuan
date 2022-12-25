from __future__ import annotations

from AnkiIn import config
from AnkiIn.config import config_updater, dict as conf, update_config
from AnkiIn.helper.formatHelper import remove_suffix
from AnkiIn.log import parser_logger as logger
from AnkiIn.notetype_loader import discovered_notetypes
from AnkiIn.parser import markdown
from ankisiyuan.notetypes import SMQA, SQA, SCloze, SListCloze, STableCloze, SWatch
from siyuanhelper import api


tag_attr_name = "ankilink"
assets_replacement = "assets"


def update_siyuan_parser():
    global tag_attr_name
    global assets_replacement
    if "siyuan" not in conf:
        conf["siyuan"] = {}
    tag_attr_name = conf["siyuan"].get("custom_attr_name", "custom-ankilink")
    assets_replacement = conf["siyuan"].get("assets_replacement", "assets")


discovered_notetypes += [SQA, SMQA, SCloze, SListCloze, STableCloze, SWatch]
config_updater.append((update_siyuan_parser, 5))
update_config()


def spec_format(text: str) -> str:
    global assets_replacement
    lines = [x for x in text.splitlines() if x != ""]
    text = ""
    for x in lines:
        if x.startswith(" "):
            # duplicate leading space for lists
            p = 0
            while x[p] == " ":
                p = p + 1
            x = x[:p] + x[:p] + x[p:]
        text = text + x + "\n"
    text = remove_suffix(text, "\n")
    text = text.replace(r"(assets/", f"({assets_replacement}/")
    return text


async def add_note(block: api.SiyuanBlock, note_list: list[api.SiyuanBlock]) -> None:
    # should pass in full block!
    text = spec_format(block.markdown)
    note = markdown.get_note(text, extra_params={"SiyuanID": block.id})
    if note is None:
        return
    note_list.append(note)


async def sync(last_sync_time: str) -> None:
    global tag_attr_name
    siyuan = api.Siyuan(token=conf["siyuan"].get("api_token", ""))
    note_list: list[api.SiyuanBlock] = []
    subs = await siyuan.get_blocks_by_sql(
        f"WHERE parent_id in (SELECT block_id FROM attributes WHERE name='{tag_attr_name}') AND updated>'{last_sync_time}'",
        full=True,
    )
    parents: dict[str, api.SiyuanBlock] = {}
    for x in subs:
        try:
            if x.parent_id not in parents:
                await (await x.parent).ensure()
                parents[x.parent_id] = await x.parent
            attr_conf = await parents[x.parent_id].attrs.get(tag_attr_name, "")
            old_conf = config.parse_config(attr_conf)
            await add_note(x, note_list)
            config.execute_config(old_conf)
        except Exception as e:
            logger.warning(
                f"An error occurred while parsing config.\nSiyuanID:{x.parent_id}\nProperty:\n{attr_conf}\nExpcetion:{e.with_traceback()}"
            )

    await siyuan.close()
    return note_list
