import asyncio

from AnkiIn import config
from AnkiIn.config import config_updater, dict as conf, update_config
from AnkiIn.helper.formatHelper import remove_suffix
from AnkiIn.log import parser_logger as logger
from AnkiIn.notetype_loader import discovered_notetypes
from AnkiIn.parser import markdown
from siyuanhelper import api

from ..notetypes import SMQA, SQA, SCloze, SListCloze, STableCloze, SWatch


# class SyntaxNode:
#     def __init__(self, id: str, parent: None | str = None, sons: None | list = None):
#         self.id = id
#         self.parent = parent
#         self.sons = sons
#         if self.sons is None:
#             self.sons = []


# link = {}
# is_added = {}
# roots = []
# note_list = []


# async def build_tree(now: str, siyuan: api.Siyuan):
#     # print("visit:{}".format(now))
#     # print("build tree")
#     # print(get_col_by_id(now, "markdown"))
#     now_node = SyntaxNode(now)
#     block = await siyuan.get_block_by_id(now)
#     link[now] = now_node
#     try:
#         if await block.attrs.get(tag_attr_name) != "":
#             roots.append(now_node)
#             return now_node
#     except Exception:
#         logger.exception(f"Exception occurred! Invalid Siyuan ID {now}")
#         logger.exception(Exception)
#     fa_id = await siyuan.get_parent_id_by_id(now)
#     if fa_id == "":
#         return now_node
#     # print("son: {} fa:{}".format(now, fa_id))
#     fa = link.get(fa_id)
#     if fa is None:
#         fa = await build_tree(fa_id, siyuan)
#     now_node.parent = fa
#     # print("fa {} added son {}".format(fa.id, now_node.id))
#     fa.sons.append(now_node)
#     # print("fa {} sons:".format(fa.id))
#     # print([x.id for x in fa.sons])
#     return now_node


# async def sync(last_time: str):
#     # session = aiohttp.ClientSession()
#     # set_session(session)
#     global siyuan
#     siyuan = api.Siyuan(token=conf["siyuan"].get("api_token", ""))
#     link.clear()
#     is_added.clear()
#     roots.clear()
#     note_list.clear()
#     all_origin_blocks = await siyuan.sql_query(
#         f"SELECT id FROM blocks where updated>'{last_time}' and type='p'"
#     )
#     all_blocks = [x["id"] for x in all_origin_blocks]
#     # print(all_blocks)
#     tasks = []
#     for x in all_blocks:
#         tasks.append(asyncio.create_task(build_tree(x, siyuan)))
#     await asyncio.tasks.gather(*tasks)
#     # print([x.id for x in roots])
#     # print([get_col_by_id(x.id,"markdown") for x in roots])
#     for x in roots:
#         await dfs(x, siyuan)
#     await siyuan.close()
#     return note_list


# async def dfs(now: SyntaxNode, siyuan: api.Siyuan):
#     # print("dfs: " + now.id)
#     # print([x.id for x in now.sons])
#     current_config = None
#     config_backup = None
#     try:
#         attrs = await siyuan.get_attrs_by_id(now.id)
#         if "custom-ankilink" not in attrs:
#             logger.debug(f"Siyuan Block {now.id} has no ankilink property.")
#         else:
#             current_config = attrs.get(tag_attr_name)
#             config_backup = config.parse_config(current_config)
#     except Exception as e:
#         logger.warning(
#             f"An error occurred while parsing config.\nSiyuanID:{now.id}\nProperty:\n{current_config}\nExpcetion:{e.with_traceback()}"
#         )
#     if len(now.sons) == 0:
#         await handle(now, siyuan)
#     else:
#         for x in now.sons:
#             await dfs(x, siyuan)
#     if config_backup is not None:
#         config.execute_config(config_backup)


# async def handle(now: SyntaxNode, siyuan: api.Siyuan):
#     fa = await siyuan.get_parent_id_by_id(now.id)
#     if fa == "":
#         await add_note(now.id, siyuan)
#         return
#     now_block = await siyuan.get_block_by_id(now.id)
#     fa_block = await siyuan.get_block_by_id(fa)
#     await now_block.ensure()
#     if now_block.type == "i" and fa_block.type == "i":
#         await handle(now.parent, siyuan)
#     else:
#         await add_note(now.id, siyuan)


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
        full=True
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
