
from random import randint
from asyncio import sleep
from os import execl
import sys
from userbot import BOTLOG, BOTLOG_CHATID, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot.main import PLUGIN_MESAJLAR

from userbot.language import get_value
LANG = get_value("misc")

# ================================================


@register(outgoing=True, pattern="^.resend")
async def resend(event):
    await event.delete()
    m = await event.get_reply_message()
    if not m:
        event.edit(LANG['REPLY_TO_FILE'])
        return
    await event.respond(m)


@register(outgoing=True, pattern="^.random")
async def randomise(items):
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            LANG['NEED_MUCH_DATA_FOR_RANDOM']
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit(f"**{LANG['QUERY']}: **\n`" + items.text[8:] + f"`\n**{LANG['RESULT']}: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ .sleep komandası TGUSERBOT'u yatızdırar :) """
    if " " not in time.pattern_match.group(1):
        await time.reply(LANG['SLEEP_DESC'])
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit(LANG['SLEEPING'])
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "Botu" + str(counter) + "saniyə yatızdırdın.",
            )
        await sleep(counter)
        await time.edit(LANG['GOODMORNIN_YALL'])


@register(outgoing=True, pattern="^.shutdown$")
async def shutdown(event):
    """ .shutdown komandası botu söndrər :( """
    await event.client.send_file(event.chat_id, 'https://www.winhistory.de/more/winstart/mp3/winxpshutdown.mp3', caption=LANG['GOODBYE_MFRS'], voice_note=True)
    await event.delete()

    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot söndürüldü.")
    try:
        await bot.disconnect()
    except BaseException:
        pass


@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit(PLUGIN_MESAJLAR['restart'])
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, f"#RESTART\n{PLUGIN_MESAJLAR['restart']}")

    try:
        await bot.disconnect()
    except BaseException:
        pass

    execl(sys.executable, sys.executable, *sys.argv)


@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    """ .support komandası support qrupunun linkini verer. """
    await wannahelp.edit(LANG['SUPPORT_GROUP'])


@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit("**@TheOksigen -  @TurkNaxcivanski - @Xwarn**")


@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.client.send_message(e.chat_id,
                                "https://github.com/XTQ067/kartof#readme",
                                link_preview=False)


@register(outgoing=True, pattern="^.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(
    outgoing=True,
    pattern="^.repo$")
async def repo(e):
    await e.edit(
        "**->** [N Σ O N Repo.](https://github.com/XTQ067/kartof) **<-**", link_preview=False)

CmdHelp('misc').add_command(
    'random',
    '<əşya1> <əşya2>',
    'Yazdığınız əşyalardan random birini seçər',
    'random YarasaUserBot Əla İşləyir').add_command(
        'sleep',
        '<vaxt>',
        'UserBot\'u yazdığınız saniyə qədər yatızdırar',
        'sleep 20').add_command(
            'shutdown',
            None,
            'Botu Söndürər.').add_command(
                'repo',
                None,
                'UseBot\'un GitHub reposunun linki.').add_command(
                    'readme',
                    None,
                    'UserBot\'un GitHub\'dakı README.md faylının linki.').add_command(
                        'creator',
                        None,
                        'Bu botu kim hazırlayıb?').add_command(
                            'repeat',
                            '<rəqəm> <mətn>',
                            'Bir mətni müəyyən sayda təkrar edər. Spam komandası ilə qarışdırma.').add_command(
                                'restart',
                                None,
                                'Botu yenidən başladar.').add_command(
                                    'resend',
                                    None,
                                    'Bir medianı yenidən göndərər.').add()
