
from userbot.events import register 
from userbot import BOTLOG, bot, BOTLOG_CHATID
import asyncio
import os
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.cmdhelp import CmdHelp
from time import sleep as t
from asyncio import sleep
from random import choice
from random import randint
import random

# ------------------------------------------------ #

@register(outgoing=True, pattern=r"^.bo[sş]luq")
async def _(e):
    await e.delete()
    await e.reply('ㅤ')


@register(outgoing=True, pattern="^:/(?: |$)(.*)", ignore_unsafe=True)
async def _(b):
    """  ;)"""
    uio = ["/", "\\"]
    for i in range(1, 19):
        t(0.35)
        await b.edit(":" + uio[i % 2])


@register(pattern=r".scam(?: |$)(.*)", outgoing=True)
async def scam(event):
    options = ['typing', 'contact', 'game', 'location', 'voice', 'round', 'video','photo', 'document', 'cancel']
    input_str = event.pattern_match.group(1)
    args = input_str.split()
    if len(args) == 0:
        scam_action = choice(options)
        scam_time = randint(30, 60)
    elif len(args) == 1:
        try:
            scam_action = str(args[0]).lower()
            scam_time = randint(30, 60)
        except ValueError:
            scam_action = choice(options)
            scam_time = int(args[0])
    elif len(args) == 2:
        scam_action = str(args[0]).lower()
        scam_time = int(args[1])
    else:
        await event.edit("Invalid Syntax !!")
        return
    try:
        if scam_time > 0:
            await event.delete()
            async with event.client.action(event.chat_id, scam_action):
                await sleep(scam_time)
    except BaseException:
        return


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    """ . """
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.edit("Mənə bir mətin ver!")
        return
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""
    await typew.edit(typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(e):

    if e.fwd_from:
        return
    ttss = e.pattern_match.group(1)
    rep_msg = None
    if e.is_reply:
        rep_msg = await e.get_reply_message()
    if len(ttss) < 1:
        if e.is_reply:
            ttss = rep_msg.text
        else:
            await e.edit("**Səsə çevirmək üçün .tts <söz/mətn> bu şəkildə yaz.**")
            return

    await e.edit(f"`Səsə çevrilir...`")
    chat = "@MrTTSbot"
    async with bot.conversation(chat) as conv:
        try:
            await conv.send_message(f"/tomp3 {ttss}")
            ses = await conv.wait_event(events.NewMessage(incoming=True, from_users=1678833172), timeout=10)
            await e.client.send_read_acknowledge(conv.chat_id)
            indir = await ses.download_media()
            voice = await asyncio.create_subprocess_shell(f"ffmpeg -i '{indir}' -c:a libopus 'MrTTSbot.ogg'")
            await voice.communicate()
            if os.path.isfile("MrTTSbot.ogg"):
                await e.client.send_file(e.chat_id, file="MrTTSbot.ogg", voice_note=True, reply_to=rep_msg)
                await e.delete()
                os.remove("MrTTSbot.ogg")
            else:
                await e.edit("`Bir xəta yarandı! ☹️`")

            if BOTLOG:
                await e.client.send_message(
                    BOTLOG_CHATID, "**Mətniniz uğurla səsə çevrildi!**")
        except YouBlockedUserError:
            await e.reply(f"**Hmm, deyəsən, {chat} blok edibsən. Zəhmət olmasa onu blokdan çıxart.**")
            return
        except asyncio.TimeoutError:
            await e.edit("`Botdan cavab ala bilmədim.` 😕")

Help = CmdHelp("neonmisc")
Help.add_command("type", "«Söz/Mətn»", "Daktilo kimi yazmaq.")
Help.add_command("boşluq", None, "Boş mesaj.")
Help.add_command(':/',None,'Reflex.')
Help.add_command('scam','<hərəkət> <vaxt>',"Saxta hərəkətlər yaradın.\nHazırda mövcud olan hərəkətlər: (typing, contact, game, location, voice, round, video, photo, document, cancel")
Help.add()
