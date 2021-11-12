from AnkiIn.note import Note
from AnkiIn.model import Model
from AnkiIn.config import dict as conf
from AnkiIn.config import config_updater
from AnkiIn.log import notetype_logger as log


notetype_name = "SWatch"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None
enable = None


def update_swatch_config():
    global settings, priority, enable

    priority = settings.get("priority", 1)
    enable = settings.get("enable", False)


config_updater.append((update_swatch_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return enable and len(lines) >= 1


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    return SWatchNote(front=text, SiyuanID=extra_params["SiyuanID"], deck=deck, tags=tags)


BACK = r"""{{FrontSide}}
<hr id=answer>
<a href="siyuan://blocks/{{SiyuanID}}">Open in SiYuan</a>
"""

CSS = r""".card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}
ul {
display: inline-block;
text-align: left;
}
ol {
display: inline-block;
text-align: left;
}
"""

MODELNAME = "SAnkiLink-Watch"
MODELID = 1195191921

_model = Model(
    modelId=MODELID,
    modelName=MODELNAME,
    fields=["Front", "SiyuanID"],
    templates=[
        {
            'Name': 'Card 1',
            'Front': '{{Front}}',
            'Back': BACK
        }
    ],
    css=CSS
)


class SWatchNote(Note):
    def __init__(self, front, SiyuanID, deck, tags):
        global _model
        super().__init__(model=_model, fields={
            "Front": front, "SiyuanID": SiyuanID}, deck=deck, tags=tags)
