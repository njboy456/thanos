import contextlib
import sys
import asyncio
import os
import re
from os import system

from userbot import *
from telethon import Button, events
from . import *
import userbot
from userbot import BOTLOG_CHATID, PM_LOGGER_GROUP_ID

from telethon import Button, custom, events

from .Config import Config
from .core.logger import logging
from .core.session import THANOSPRO, tgbot
from .utils import (
    add_bot_to_logger_group,
    install_externalrepo,
    load_plugins,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("THANOSBOT")
THANOS_NAME = "✽ ᴛʜᴀɴᴏꜱ-ᴠᄅ"

bot = THANOSPRO
print(userbot.__copyright__)
print(f"Licensed under the terms of the {userbot.__license__}")

async def rishabh():
    THANOS_USER = bot.me.first_name
    The_THANOSBOY = bot.uid
    thanos_mention = f"[{THANOS_USER}](tg://user?id={The_THANOSBOY})"
    name = f"{thanos_mention}'s Assistant"
    description = f"I am Assistant Of {thanos_mention}.This Bot Can Help U To Chat With My Master"
    starkbot = await THANOSPRO.tgbot.get_me()
    bot_name = starkbot.first_name
    botname = f"@{starkbot.username}"
    if bot_name.endswith("Assistant"):
        print("Bot Starting")
    else:
        try:
            await bot.send_message("@BotFather", "/setinline")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", THANOS_NAME)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setname")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", name)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setdescription")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", description)
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", "/setuserpic")
            await asyncio.sleep(1)
            await bot.send_message("@BotFather", botname)
            await asyncio.sleep(1)
            await bot.send_file(
                "@BotFather", "userbot/helpers/resources/pics/main.jpg"
            )
            await asyncio.sleep(2)
        except Exception as e:
            print(e)


cmdhr = Config.COMMAND_HAND_LER

try:
    LOGS.info("Starting Userbot")
    THANOSPRO.loop.run_until_complete(setup_bot())
    LOGS.info("TG Bot Startup Completed")
except Exception as e:
    LOGS.error(f"{e}")
    sys.exit()


async def startup_process():
    await verifyLoggerGroup()
    await load_plugins("plugins")
    await load_plugins("assistant")
    await rishabh()
    print("============================================================")
    print("Yay your userbot is officially working.!!!")
    print(
        f"Congratulation, now type {cmdhr}alive to see message if THANOSPRO is live\
        \nIf you need assistance, head to https://t.me/THANOSUserbot_support"
    )
    print("============================================================")
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    return


async def externalrepo():
    #if Config.EXTERNAL_REPO:
       # await install_externalrepo(
            #Config.EXTERNAL_REPO, Config.EXTERNAL_REPOBRANCH, "xtraplugins"
        #)
    #if Config.THANOSABUSE :
       # await install_externalrepo(
           # Config.THANOSABUSE _REPO, Config.THANOSABUSE _REPOBRANCH, "badcatext"
        #)
    if Config.VCMODE:
        await install_externalrepo(
            "https://github.com/Tgcatub/THANOSVCPlayer", "test", "catvc"
        )


THANOSPRO.loop.run_until_complete(startup_process())

THANOSPRO.loop.run_until_complete(externalrepo())

if len(sys.argv) in {1, 3, 4}:
    with contextlib.suppress(ConnectionError):
        THANOSPRO.run_until_disconnected()
else:
    THANOSPRO.disconnect()
