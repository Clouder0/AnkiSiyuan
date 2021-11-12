from AnkiIn.note import Note
from AnkiIn.model import Model
from AnkiIn.config import dict as conf
from AnkiIn.config import config_updater
from AnkiIn.log import notetype_logger as log
from AnkiIn.notetypes.Cloze import get as super_get
from AnkiIn.notetypes.Cloze import check as super_check
from AnkiIn.notetypes.Cloze import ClozeNote


notetype_name = "SCloze"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_siyuan_cloze_config():
    global settings, priority

    priority = settings.get("priority", 22)


config_updater.append((update_siyuan_cloze_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return super_check(lines=lines, extra_params=extra_params)


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    return SClozeNote(extra_params["SiyuanID"], super_get(text=text, deck=deck, tags=tags, extra_params=extra_params))


CSS = r""".card {
  font-family: arial;
  font-size: 20px;
  text-align: center;
  color: black;
  background-color: white;
}

.cloze {
 font-weight: bold;
 color: blue;
}
.nightMode .cloze {
 color: lightblue;
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

BACK = r"""{{cloze:Text}}
</br>
<a href="siyuan://blocks/{{SiyuanID}}">Open in SiYuan</a>"""

MODELNAME = "SAnkiLink-Cloze"
MODELID = 1146141120

_model = Model(
    modelId=MODELID,
    modelName=MODELNAME,
    isCloze=1,
    fields=["Text", "Back Extra", "SiyuanID"],
    templates=[
        {
            "Name": "Cloze",
            "Front": "{{cloze:Text}}",
            "Back": BACK
        }
    ],
    css=CSS
)


class SClozeNote(ClozeNote):
    def __init__(self, SiyuanID: str, text: str, deck, tags):
        global _model
        super().__init__(text=text, deck=deck, tags=tags)
        self.model = _model
        self["SiyuanID"] = SiyuanID

    def __init__(self, SiyuanID: str, Note):
        global _model
        self.__dict__.update(Note.__dict__)
        self.model = _model
        self["SiyuanID"] = SiyuanID
