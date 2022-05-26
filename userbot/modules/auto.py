import asyncio
import time
from telethon.tl import functions
from userbot import ASYNC_POOL
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot.language import get_value
LANG = get_value("auto")


@register(outgoing=True, pattern="^.auto ?(.*)")
async def auto(event):
    metod = event.pattern_match.group(1).lower()

    if str(metod) not in ("ad", "bio"):
        await event.edit(LANG['INVALID_TYPE'])
        return

    if metod in ASYNC_POOL:
        await event.edit(LANG['ALREADY'] % metod)
        return

    await event.edit(LANG['SETTING'] % metod)
    if metod == "ad":
        HM = time.strftime("%H:%M")
        await event.client(functions.account.UpdateProfileRequest(last_name=LANG['NAME'] % HM))
    elif metod == "bio":
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M")
        Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK']
        await event.client(functions.account.UpdateProfileRequest(about=Bio))
    await event.edit(LANG['SETTED'] % metod)
    ASYNC_POOL.append(metod)
    while metod in ASYNC_POOL:
        try:
            if metod == "ad":
                HM = time.strftime("%H:%M")
                await event.client(functions.account.UpdateProfileRequest(last_name=LANG['NAME'] % HM))
            elif metod == "bio":
                DMY = time.strftime("%d.%m.%Y")
                HM = time.strftime("%H:%M")

                Bio = LANG['BIO'].format(tarih=DMY, saat=HM) + LANG['NICK']
                await event.client(functions.account.UpdateProfileRequest(about=Bio))

            await asyncio.sleep(60)
        except BaseException:
            return

Help = CmdHelp('auto')
Help.add_command('auto', 'ad vəya bio', 'Adınıza və ya Bionuza bir saat əlavə edər və bu saat avtomatik dəyişər.', '.auto ad/bio')
Help.add()
