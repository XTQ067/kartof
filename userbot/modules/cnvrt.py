import asyncio
import os
import time
import math
from datetime import datetime
from userbot import TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register
from userbot.cmdhelp import CmdHelp



def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


async def progress(current, total, event, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}] {2}%\n".format(
            ''.join(["▰" for i in range(math.floor(percentage / 10))]),
            ''.join(["▱" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await event.edit("{}\n{}: `{}`\n{}".format(
                type_of_ps, LANG['FILENAME'], file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))




def humanbytes(size):
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"



def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + f" {LANG['DAY']}, ") if days else "") + \
        ((str(hours) + " saat, ") if hours else "") + \
        ((str(minutes) + " dakika, ") if minutes else "") + \
        ((str(seconds) + " saniye, ") if seconds else "") + \
        ((str(milliseconds) + " milisaniye, ") if milliseconds else "")
    return tmp[:-2]




@register(pattern=r"^\.cnvrt(?: |$)(.*)", outgoing=True)
@register(pattern=r"^\.[cç]evir(?: |$)(.*)", outgoing=True)
async def _(event):
    if not event.reply_to_msg_id:
        await event.edi("**Mesaja cavab ver.** ❌")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("**Musiqiyə cavab ver.** 🎵")
        return
    event = await event.edit("**Hazırlanır...** ⏳")
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await event.client.download_media(
            reply_message, TEMP_DOWNLOAD_DIRECTORY, progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            ),
        )
    except Exception as e:
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit(
            "{} // {}".format(downloaded_file_name, ms)
        )
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if downloaded_file_name.endswith((".mp3", "m4a", "mp4")):
            new_required_file_caption = "." + str(round(time.time())) + ".ogg"
            new_required_file_name = (
                TEMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name,
            ]
            voice_note = True
            supports_streaming = True
        elif downloaded_file_name.endswith((".ogg", "m4a", "mp4")):
            new_required_file_caption = "." + str(round(time.time())) + ".mp3"
            new_required_file_name = (
                TEMP_DOWNLOAD_DIRECTORY + "/" + new_required_file_caption
            )
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name,
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("**Dəstəklənməyən növ fayl.**")
            os.remove(downloaded_file_name)
            return
        process = await asyncio.create_subprocess_exec(
            *command_to_run,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        stderr.decode().strip()
        stdout.decode().strip()
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            force_document = False
            await event.client.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                ),
            )
            os.remove(new_required_file_name)
            await event.delete()

Help = CmdHelp("cnvrt")
Help.add_command("cnvrt", None, "Mp3 formatını səsə, səs formatını mp3-ə çevirər.")
Help.add()