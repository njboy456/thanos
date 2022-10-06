import base64
import contextlib
from asyncio import sleep

from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.utils import get_display_name

from .. import THANOSPRO
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper import broadcast_sql as sql
from . import BOTLOG, BOTLOG_CHATID

plugin_thanosegory = "tools"

LOGS = logging.getLogger(__name__)


@THANOSPRO.thanos_cmd(
    pattern="msgto(?:\s|$)([\s\S]*)",
    command=("msgto", plugin_thanosegory),
    info={
        "header": "To message to person or to a chat.",
        "description": "Suppose you want to message directly to a person/chat from a paticular chat. Then simply reply to a person with this cmd and text or to a text with cmd and username/userid/chatid,",
        "usage": [
            "{tr}msgto <username/userid/chatid/chatusername> reply to message",
            "{tr}msgto <username/userid/chatid/chatusername> <text>",
        ],
        "examples": "{tr}msgto @THANOSBOTot just a testmessage",
    },
)
async def thanosbroadcast_add(event):
    "To message to person or to a chat."
    user, reason = await get_user_from_event(event)
    reply = await event.get_reply_message()
    if not user:
        return
    if not reason and not reply:
        return await edit_delete(
            event, "__What should i send to the person. reply to msg or give text__"
        )
    if reply and reason and user.id != reply.sender_id:
        if BOTLOG:
            msg = await event.client.send_message(BOTLOG_CHATID, reason)
            await event.client.send_message(
                BOTLOG_CHATID,
                "The replied message was failed to send to the user. Confusion between to whom it should send.",
                reply_to=msg.id,
            )
        msglink = await event.clienr.get_msg_link(msg)
        return await edit_or_reply(
            event,
            f"__Sorry! Confusion between users to whom should i send the person mentioned in message or to the person replied. text message was logged in [log group]({msglink}). you can resend message from there__",
        )
    if reason:
        msg = await event.client.send_message(user.id, reason)
    else:
        msg = await event.client.send_message(user.id, reply)
    await edit_delete(event, "__Successfully sent the message.__")


@THANOSPRO.thanos_cmd(
    pattern="addto(?:\s|$)([\s\S]*)",
    command=("addto", plugin_thanosegory),
    info={
        "header": "Will add the specific chat to the mentioned thanosegory",
        "usage": "{tr}addto <thanosegory name>",
        "examples": "{tr}addto test",
    },
)
async def thanosbroadcast_add(event):
    "To add the chat to the mentioned thanosegory"
    thanosinput_str = event.pattern_match.group(1)
    if not thanosinput_str:
        return await edit_delete(
            event,
            "In which thanosegory should i add this chat",
            parse_mode=_format.parse_pre,
        )
    keyword = thanosinput_str.lower()
    if check := sql.is_in_broadcastlist(keyword, event.chat_id):
        return await edit_delete(
            event,
            f"This chat is already in this thanosegory {keyword}",
            parse_mode=_format.parse_pre,
        )
    sql.add_to_broadcastlist(keyword, event.chat_id)
    await edit_delete(
        event,
        f"This chat is Now added to thanosegory {keyword}",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {get_display_name(await event.get_chat())} is added to thanosegory {keyword}",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is added to thanosegory {keyword}",
                parse_mode=_format.parse_pre,
            )


@THANOSPRO.thanos_cmd(
    pattern="list(?:\s|$)([\s\S]*)",
    command=("list", plugin_thanosegory),
    info={
        "header": "will show the list of all chats in the given thanosegory",
        "usage": "{tr}list <thanosegory name>",
        "examples": "{tr}list test",
    },
)
async def thanosbroadcast_list(event):
    "To list the all chats in the mentioned thanosegory."
    thanosinput_str = event.pattern_match.group(1)
    if not thanosinput_str:
        return await edit_delete(
            event,
            "Which thanosegory Chats should i list ?\nCheck .listall",
            parse_mode=_format.parse_pre,
        )
    keyword = thanosinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    if no_of_chats == 0:
        return await edit_delete(
            event,
            f"There is no thanosegory with name {keyword}. Check '.listall'",
            parse_mode=_format.parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    thanosevent = await edit_or_reply(
        event, f"Fetching info of the thanosegory {keyword}", parse_mode=_format.parse_pre
    )
    resultlist = f"**The thanosegory '{keyword}' have '{no_of_chats}' chats and these are listed below :**\n\n"
    errorlist = ""
    for chat in chats:
        try:
            chatinfo = await event.client.get_entity(int(chat))
            try:
                if chatinfo.broadcast:
                    resultlist += f" 👉 📢 **Channel** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
                else:
                    resultlist += f" 👉 👥 **Group** \n  •  **Name : **{chatinfo.title} \n  •  **id : **`{int(chat)}`\n\n"
            except AttributeError:
                resultlist += f" 👉 👤 **User** \n  •  **Name : **{chatinfo.first_name} \n  •  **id : **`{int(chat)}`\n\n"
        except Exception:
            errorlist += f" 👉 __This id {int(chat)} in database probably you may left the chat/channel or may be invalid id.\
                            \nRemove this id from the database by using this command__ `.frmfrom {keyword} {int(chat)}` \n\n"
    finaloutput = resultlist + errorlist
    await edit_or_reply(thanosevent, finaloutput)


@THANOSPRO.thanos_cmd(
    pattern="listall$",
    command=("listall", plugin_thanosegory),
    info={
        "header": "Will show the list of all thanosegory names.",
        "usage": "{tr}listall",
    },
)
async def thanosbroadcast_list(event):
    "To list all the thanosegory names."
    if sql.num_broadcastlist_chats() == 0:
        return await edit_delete(
            event,
            "you haven't created at least one thanosegory  check info for more help",
            parse_mode=_format.parse_pre,
        )
    chats = sql.get_broadcastlist_chats()
    resultext = "**Here are the list of your thanosegory's :**\n\n"
    for i in chats:
        resultext += f" 👉 `{i}` __contains {sql.num_broadcastlist_chat(i)} chats__\n"
    await edit_or_reply(event, resultext)


@THANOSPRO.thanos_cmd(
    pattern="sendto(?:\s|$)([\s\S]*)",
    command=("sendto", plugin_thanosegory),
    info={
        "header": "will send the replied message to all chats in the given thanosegory",
        "usage": "{tr}sendto <thanosegory name>",
        "examples": "{tr}sendto test",
    },
)
async def thanosbroadcast_send(event):
    "To send the message to all chats in the mentioned thanosegory."
    thanosinput_str = event.pattern_match.group(1)
    if not thanosinput_str:
        return await edit_delete(
            event,
            "To which thanosegory should i send this message",
            parse_mode=_format.parse_pre,
        )
    reply = await event.get_reply_message()
    thanos = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await edit_delete(
            event,
            "what should i send to to this thanosegory ?",
            parse_mode=_format.parse_pre,
        )
    keyword = thanosinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    group_ = Get(thanos)
    if no_of_chats == 0:
        return await edit_delete(
            event,
            f"There is no thanosegory with name {keyword}. Check '.listall'",
            parse_mode=_format.parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    thanosevent = await edit_or_reply(
        event,
        "sending this message to all groups in the thanosegory",
        parse_mode=_format.parse_pre,
    )
    with contextlib.suppress(BaseException):
        await event.client(group_)
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.send_message(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`The message was sent to {i} chats out of {no_of_chats} chats in thanosegory {keyword}.`"
    await edit_delete(thanosevent, resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"A message is sent to {i} chats out of {no_of_chats} chats in thanosegory {keyword}",
            parse_mode=_format.parse_pre,
        )


@THANOSPRO.thanos_cmd(
    pattern="fwdto(?:\s|$)([\s\S]*)",
    command=("fwdto", plugin_thanosegory),
    info={
        "header": "Will forward the replied message to all chats in the given thanosegory",
        "usage": "{tr}fwdto <thanosegory name>",
        "examples": "{tr}fwdto test",
    },
)
async def thanosbroadcast_send(event):
    "To forward the message to all chats in the mentioned thanosegory."
    thanosinput_str = event.pattern_match.group(1)
    if not thanosinput_str:
        return await edit_delete(
            event,
            "To which thanosegory should i send this message",
            parse_mode=_format.parse_pre,
        )
    reply = await event.get_reply_message()
    thanos = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    if not reply:
        return await edit_delete(
            event,
            "what should i send to to this thanosegory ?",
            parse_mode=_format.parse_pre,
        )
    keyword = thanosinput_str.lower()
    no_of_chats = sql.num_broadcastlist_chat(keyword)
    group_ = Get(thanos)
    if no_of_chats == 0:
        return await edit_delete(
            event,
            f"There is no thanosegory with name {keyword}. Check '.listall'",
            parse_mode=_format.parse_pre,
        )
    chats = sql.get_chat_broadcastlist(keyword)
    thanosevent = await edit_or_reply(
        event,
        "sending this message to all groups in the thanosegory",
        parse_mode=_format.parse_pre,
    )
    with contextlib.suppress(BaseException):
        await event.client(group_)
    i = 0
    for chat in chats:
        try:
            if int(event.chat_id) == int(chat):
                continue
            await event.client.forward_messages(int(chat), reply)
            i += 1
        except Exception as e:
            LOGS.info(str(e))
        await sleep(0.5)
    resultext = f"`The message was sent to {i} chats out of {no_of_chats} chats in thanosegory {keyword}.`"
    await edit_delete(thanosevent, resultext)
    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"A message is forwared to {i} chats out of {no_of_chats} chats in thanosegory {keyword}",
            parse_mode=_format.parse_pre,
        )


@THANOSPRO.thanos_cmd(
    pattern="rmfrom(?:\s|$)([\s\S]*)",
    command=("rmfrom", plugin_thanosegory),
    info={
        "header": "Will remove the specific chat to the mentioned thanosegory",
        "usage": "{tr}rmfrom <thanosegory name>",
        "examples": "{tr}rmfrom test",
    },
)
async def thanosbroadcast_remove(event):
    "To remove the chat from the mentioned thanosegory"
    thanosinput_str = event.pattern_match.group(1)
    if not thanosinput_str:
        return await edit_delete(
            event,
            "From which thanosegory should i remove this chat",
            parse_mode=_format.parse_pre,
        )
    keyword = thanosinput_str.lower()
    check = sql.is_in_broadcastlist(keyword, event.chat_id)
    if not check:
        return await edit_delete(
            event,
            f"This chat is not in the thanosegory {keyword}",
            parse_mode=_format.parse_pre,
        )
    sql.rm_from_broadcastlist(keyword, event.chat_id)
    await edit_delete(
        event,
        f"This chat is Now removed from the thanosegory {keyword}",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {get_display_name(await event.get_chat())} is removed from thanosegory {keyword}",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is removed from thanosegory {keyword}",
                parse_mode=_format.parse_pre,
            )


@THANOSPRO.thanos_cmd(
    pattern="frmfrom(?:\s|$)([\s\S]*)",
    command=("frmfrom", plugin_thanosegory),
    info={
        "header": " To force remove the given chat from a thanosegory.",
        "description": "Suppose if you are muted or group/channel is deleted you cant send message there so you can use this cmd to the chat from that thanosegory",
        "usage": "{tr}frmfrom <thanosegory name> <chatid>",
        "examples": "{tr}frmfrom test -100123456",
    },
)
async def thanosbroadcast_remove(event):
    "To force remove the given chat from a thanosegory."
    thanosinput_str = event.pattern_match.group(1)
    if not thanosinput_str:
        return await edit_delete(
            event,
            "From which thanosegory should i remove this chat",
            parse_mode=_format.parse_pre,
        )
    args = thanosinput_str.split(" ")
    if len(args) != 2:
        return await edit_delete(
            event,
            "Use proper syntax as shown .frmfrom thanosegory_name groupid",
            parse_mode=_format.parse_pre,
        )
    try:
        groupid = int(args[0])
        keyword = args[1].lower()
    except ValueError:
        try:
            groupid = int(args[1])
            keyword = args[0].lower()
        except ValueError:
            return await edit_delete(
                event,
                "Use proper syntax as shown .frmfrom thanosegory_name groupid",
                parse_mode=_format.parse_pre,
            )
    keyword = keyword.lower()
    check = sql.is_in_broadcastlist(keyword, groupid)
    if not check:
        return await edit_delete(
            event,
            f"This chat {groupid} is not in the thanosegory {keyword}",
            parse_mode=_format.parse_pre,
        )
    sql.rm_from_broadcastlist(keyword, groupid)
    await edit_delete(
        event,
        f"This chat {groupid} is Now removed from the thanosegory {keyword}",
        parse_mode=_format.parse_pre,
    )
    chat = await event.get_chat()
    if BOTLOG:
        try:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The Chat {get_display_name(await event.get_chat())} is removed from thanosegory {keyword}",
                parse_mode=_format.parse_pre,
            )
        except Exception:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"The user {chat.first_name} is removed from thanosegory {keyword}",
                parse_mode=_format.parse_pre,
            )


@THANOSPRO.thanos_cmd(
    pattern="delc(?:\s|$)([\s\S]*)",
    command=("delc", plugin_thanosegory),
    info={
        "header": "To Deletes the thanosegory completely from database",
        "usage": "{tr}delc <thanosegory name>",
        "examples": "{tr}delc test",
    },
)
async def thanosbroadcast_delete(event):
    "To delete a thanosegory completely."
    thanosinput_str = event.pattern_match.group(1)
    check1 = sql.num_broadcastlist_chat(thanosinput_str)
    if check1 < 1:
        return await edit_delete(
            event,
            f"Are you sure that there is thanosegory {thanosinput_str}",
            parse_mode=_format.parse_pre,
        )
    try:
        sql.del_keyword_broadcastlist(thanosinput_str)
        await edit_or_reply(
            event,
            f"Successfully deleted the thanosegory {thanosinput_str}",
            parse_mode=_format.parse_pre,
        )
    except Exception as e:
        await edit_delete(
            event,
            str(e),
            parse_mode=_format.parse_pre,
        )
