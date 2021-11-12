from AnkiIn.note import Note
from AnkiIn.notetypes.QA import get as super_get
from AnkiIn.notetypes.QA import check as super_check
from AnkiIn.model import Model
from AnkiIn.config import dict as conf
from AnkiIn.config import config_updater
from AnkiIn.notetypes.QA import QANote


notetype_name = "SQA"
if notetype_name not in conf["notetype"]:
    conf["notetype"][notetype_name] = {}
settings = conf["notetype"][notetype_name]

priority = None


def update_siyuan_qa_config():
    global settings, priority

    priority = settings.get("priority", 11)


config_updater.append((update_siyuan_qa_config, 10))


def check(lines: list, extra_params={}) -> bool:
    return super_check(lines=lines, extra_params=extra_params)


def get(text: str, deck: str, tags: list, extra_params={}) -> Note:
    return SQANote(extra_params["SiyuanID"], super_get(text=text, deck=deck, tags=tags, extra_params=extra_params))


BACK = r"""{{FrontSide}}
<hr id=answer>
{{Back}}
</br>
<a href="siyuan://blocks/{{SiyuanID}}">Open in SiYuan</a>"""

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

MODELNAME = "SAnkiLink-Basic"
MODELID = 1145841921

_model = Model(
    modelId=MODELID,
    modelName=MODELNAME,
    fields=["Front", "Back", "SiyuanID"],
    templates=[
        {
            'Name': 'Card 1',
            'Front': '{{Front}}',
            'Back': BACK
        }
    ],
    css=CSS
)


class SQANote(QANote):
    def __init__(self, SiyuanID, front, back, deck, tags):
        global _model
        super.__init__(front=front, back=back, deck=deck, tags=tags)
        self.model = _model
        self["SiyuanID"] = SiyuanID

    def __init__(self, SiyuanID, Note):
        global _model
        self.__dict__.update(Note.__dict__)
        self.model = _model
        self["SiyuanID"] = SiyuanID
