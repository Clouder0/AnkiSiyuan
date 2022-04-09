from AnkiIn.helper.formatHelper import remove_suffix
from siyuanhelper.helper import PropertyNotFoundException, do_property_exist_by_id, get_parent_by_id
from siyuanhelper.helper import get_property_by_id, query_sql, get_col_by_id
from siyuanhelper.helper import set_token, set_session
from AnkiIn.parser import markdown
from AnkiIn.notetype_loader import discovered_notetypes
from ..notetypes import SQA, SMQA, SCloze, SListCloze, STableCloze, SWatch
from AnkiIn.config import update_config
from AnkiIn.config import dict as conf
from AnkiIn.config import config_updater
from AnkiIn import config
from AnkiIn.log import parser_logger as logger
import asyncio
import aiohttp


class SyntaxNode:
    def __init__(self, id: str, parent=None, sons=None):
        self.id = id
        self.parent = parent
        self.sons = sons
        if self.sons is None:
            self.sons = []


link = {}
is_added = {}
roots = []
noteList = []
tag_attr_name = "ankilink"
assets_replacement = "assets"


def update_siyuan_parser():
    global tag_attr_name
    global assets_replacement
    if "siyuan" not in conf:
        conf["siyuan"] = {}
    tag_attr_name = conf["siyuan"].get(
        "custom_attr_name", "custom-ankilink")
    assets_replacement = conf["siyuan"].get("assets_replacement", "assets")


discovered_notetypes += [SQA, SMQA, SCloze, SListCloze, STableCloze, SWatch]
config_updater.append((update_siyuan_parser, 5))
update_config()


async def build_tree(now: str):
    # print("visit:{}".format(now))
    # print("build tree")
    # print(get_col_by_id(now, "markdown"))
    now_node = SyntaxNode(now)
    link[now] = now_node
    try:
        if await do_property_exist_by_id(now, tag_attr_name):
            roots.append(now_node)
            return now_node
    except Exception:
        logger.exception("Exception occurred! Invalid Siyuan ID {}".format(now))
        logger.exception(Exception)
    fa_id = await get_parent_by_id(now)
    if fa_id == "":
        return now_node
    # print("son: {} fa:{}".format(now, fa_id))
    fa = link.get(fa_id)
    if fa is None:
        fa = await build_tree(fa_id)
    now_node.parent = fa
    # print("fa {} added son {}".format(fa.id, now_node.id))
    fa.sons.append(now_node)
    # print("fa {} sons:".format(fa.id))
    # print([x.id for x in fa.sons])
    return now_node


async def sync(last_time: str):
    # session = aiohttp.ClientSession()
    # set_session(session)
    set_token(conf["siyuan"].get("api_token", ""))
    session = aiohttp.ClientSession()
    set_session(session)
    link.clear()
    is_added.clear()
    roots.clear()
    noteList.clear()
    all_origin_blocks = await query_sql(
        r"SELECT id FROM blocks where updated>'{}' and type='p'".format(last_time))
    all_blocks = [x["id"] for x in all_origin_blocks]
    # print(all_blocks)
    tasks = []
    for x in all_blocks:
        tasks.append(asyncio.create_task(build_tree(x)))
    await asyncio.tasks.gather(*tasks)
    # print([x.id for x in roots])
    # print([get_col_by_id(x.id,"markdown") for x in roots])
    for x in roots:
        await dfs(x)
    await session.close()
    return noteList


async def dfs(now: SyntaxNode):
    # print("dfs: " + now.id)
    # print([x.id for x in now.sons])
    current_config = None
    config_backup = None
    try:
        current_config = (await get_property_by_id(
            now.id, tag_attr_name))
        config_backup = config.parse_config(current_config)
    except PropertyNotFoundException:
        logger.debug("SiyuanID:{} has no config.".format(now.id))
    # except Exception:
    #    logger.warning(
    #        "An error occurred while parsing config.\nSiyuanID:{}\nProperty:\n{}".format(now.id, current_config))
    if len(now.sons) == 0:
        # print("!!!")
        # print(get_col_by_id(now.id, "markdown"))
        # leaf
        await handle(now)
    else:
        for x in now.sons:
            await dfs(x)
    if config_backup is not None:
        config.execute_config(config_backup)


async def handle(now: SyntaxNode):
    fa = await get_parent_by_id(now.id)
    if (await get_col_by_id(now.id, "type")) == "i" or fa != "" and (await get_col_by_id(fa, "type")) == "i":
        await handle(now.parent)
    else:
        await addNote(now.id)


async def addNote(id):
    if is_added.get(id, False):
        return
    text = spec_format(await get_col_by_id(id, "markdown"))
    note = markdown.get_note(text, extra_params={"SiyuanID": id})
    if note is None:
        return
    noteList.append(note)
    is_added[id] = True


def spec_format(text: str) -> str:
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
    text = text.replace(
        r"(assets/", r"({}/".format(assets_replacement))
    return text
