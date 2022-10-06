import os

from PIL import Image

from userbot.core.logger import logging
from userbot.core.managers import edit_or_reply
from userbot.helpers.functions.vidtools import take_screen_shot
from userbot.helpers.tools import fileinfo, media_type, meme_type
from userbot.helpers.utils.utils import runcmd

LOGS = logging.getLogger(__name__)


class THANOSConverter:
    async def _media_check(self, reply, dirct, file, memetype):
        if not os.path.isdir(dirct):
            os.mkdir(dirct)
        thanosfile = os.path.join(dirct, file)
        if os.path.exists(thanosfile):
            os.remove(thanosfile)
        try:
            thanosmedia = reply if os.path.exists(reply) else None
        except TypeError:
            if memetype in ["Video", "Gif"]:
                dirct = "./temp/thanosfile.mp4"
            elif memetype == "Audio":
                dirct = "./temp/thanosfile.mp3"
            thanosmedia = await reply.download_media(dirct)
        return thanosfile, thanosmedia

    async def to_image(
        self, event, reply, dirct="./temp", file="meme.png", noedits=False, rgb=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype == "Document":
            return event, None
        thanosevent = (
            event
            if noedits
            else await edit_or_reply(
                event, "`Transfiguration Time! Converting to ....`"
            )
        )
        thanosfile, thanosmedia = await self._media_check(reply, dirct, file, memetype)
        if memetype == "Photo":
            im = Image.open(thanosmedia)
            im.save(thanosfile)
        elif memetype in ["Audio", "Voice"]:
            await runcmd(f"ffmpeg -i '{thanosmedia}' -an -c:v copy '{thanosfile}' -y")
        elif memetype in ["Round Video", "Video", "Gif"]:
            await take_screen_shot(thanosmedia, "00.00", thanosfile)
        if mediatype == "Sticker":
            if memetype == "Animated Sticker":
                thanoscmd = f"lottie_convert.py --frame 0 -if lottie -of png '{thanosmedia}' '{thanosfile}'"
                stdout, stderr = (await runcmd(thanoscmd))[:2]
                if stderr:
                    LOGS.info(stdout + stderr)
            elif memetype == "Video Sticker":
                await take_screen_shot(thanosmedia, "00.00", thanosfile)
            elif memetype == "Static Sticker":
                im = Image.open(thanosmedia)
                im.save(thanosfile)
        if thanosmedia and os.path.exists(thanosmedia):
            os.remove(thanosmedia)
        if os.path.exists(thanosfile):
            if rgb:
                img = Image.open(thanosfile)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img.save(thanosfile)
            return thanosevent, thanosfile, mediatype
        return thanosevent, None

    async def to_sticker(
        self, event, reply, dirct="./temp", file="meme.webp", noedits=False, rgb=False
    ):
        filename = os.path.join(dirct, file)
        response = await self.to_image(event, reply, noedits=noedits, rgb=rgb)
        if response[1]:
            image = Image.open(response[1])
            image.save(filename, "webp")
            os.remove(response[1])
            return response[0], filename, response[2]
        return response[0], None

    async def to_webm(
        self, event, reply, dirct="./temp", file="animate.webm", noedits=False
    ):
        # //Hope u dunt kang :/ @Jisan7509
        memetype = await meme_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Gif",
            "Video",
        ]:
            return event, None
        thanosevent = (
            event
            if noedits
            else await edit_or_reply(event, "__🎞Converting into Animated sticker..__")
        )
        thanosfile, thanosmedia = await self._media_check(reply, dirct, file, memetype)
        media = await fileinfo(thanosmedia)
        h = media["height"]
        w = media["width"]
        w, h = (-1, 512) if h > w else (512, -1)
        await runcmd(
            f"ffmpeg -to 00:00:02.900 -i '{thanosmedia}' -vf scale={w}:{h} -c:v libvpx-vp9 -crf 30 -b:v 560k -maxrate 560k -bufsize 256k -an '{thanosfile}'"
        )  # pain
        if os.path.exists(thanosmedia):
            os.remove(thanosmedia)
        if os.path.exists(thanosfile):
            return thanosevent, thanosfile
        return thanosevent, None

    async def to_gif(
        self, event, reply, dirct="./temp", file="meme.mp4", maxsize="5M", noedits=False
    ):
        memetype = await meme_type(reply)
        mediatype = await media_type(reply)
        if memetype not in [
            "Round Video",
            "Video Sticker",
            "Animated Sticker",
            "Video",
            "Gif",
        ]:
            return event, None
        thanosevent = (
            event
            if noedits
            else await edit_or_reply(
                event, "`Transfiguration Time! Converting to ....`"
            )
        )
        thanosfile, thanosmedia = await self._media_check(reply, dirct, file, memetype)
        if mediatype == "Sticker":
            if memetype == "Video Sticker":
                await runcmd(f"ffmpeg -i '{thanosmedia}' -c copy '{thanosfile}'")
            elif memetype == "Animated Sticker":
                await runcmd(f"lottie_convert.py '{thanosmedia}' '{thanosfile}'")
        if thanosmedia.endswith(".gif"):
            await runcmd(f"ffmpeg -f gif -i '{thanosmedia}' -fs {maxsize} -an '{thanosfile}'")
        else:
            await runcmd(
                f"ffmpeg -i '{thanosmedia}' -c:v libx264 -fs {maxsize} -an '{thanosfile}'"
            )
        if thanosmedia and os.path.exists(thanosmedia):
            os.remove(thanosmedia)
        if os.path.exists(thanosfile):
            return thanosevent, thanosfile
        return thanosevent, None


Convert = THANOSConverter()
