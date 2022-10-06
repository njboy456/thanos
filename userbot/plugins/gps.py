#    Credts @Mrconfused
from geopy.geocoders import Nominatim
from telethon.tl import types

from userbot import THANOSPRO

from ..core.managers import edit_or_reply
from ..helpers import reply_id

plugin_thanosegory = "extra"


@THANOSPRO.thanos_cmd(
    pattern="gps ([\s\S]*)",
    command=("gps", plugin_thanosegory),
    info={
        "header": "To send the map of the given lothanosion.",
        "usage": "{tr}gps <place>",
        "examples": "{tr}gps Hyderabad",
    },
)
async def gps(event):
    "Map of the given lothanosion."
    reply_to_id = await reply_id(event)
    input_str = event.pattern_match.group(1)
    thanosevent = await edit_or_reply(event, "`finding.....`")
    geolothanosor = Nominatim(user_agent="THANOSBOT")
    if geoloc := geolothanosor.geocode(input_str):
        lon = geoloc.longitude
        lat = geoloc.latitude
        await event.client.send_file(
            event.chat_id,
            file=types.InputMediaGeoPoint(types.InputGeoPoint(lat, lon)),
            caption=f"**Lothanosion : **`{input_str}`",
            reply_to=reply_to_id,
        )
        await thanosevent.delete()
    else:
        await thanosevent.edit("`i coudn't find it`")
