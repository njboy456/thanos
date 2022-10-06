from userbot import THANOSPRO

from ..core.managers import edit_or_reply
from ..helpers.utils import _format

plugin_thanosegory = "tools"

# yaml_format is ported from uniborg
@THANOSPRO.thanos_cmd(
    pattern="json$",
    command=("json", plugin_thanosegory),
    info={
        "header": "To get details of that message in json format.",
        "usage": "{tr}json reply to message",
    },
)
async def _(event):
    "To get details of that message in json format."
    thanosevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = thanosevent.stringify()
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)


@THANOSPRO.thanos_cmd(
    pattern="yaml$",
    command=("yaml", plugin_thanosegory),
    info={
        "header": "To get details of that message in yaml format.",
        "usage": "{tr}yaml reply to message",
    },
)
async def _(event):
    "To get details of that message in yaml format."
    thanosevent = await event.get_reply_message() if event.reply_to_msg_id else event
    the_real_message = _format.yaml_format(thanosevent)
    await edit_or_reply(event, the_real_message, parse_mode=_format.parse_pre)
