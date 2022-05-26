
from userbot.language import get_value
from platform import uname
from userbot import CMD_HELP, NEON_VERSION, WHITELIST, yetimler, nusrte
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import version
from platform import python_version
from userbot.cmdhelp import CmdHelp

DEFAULTUSER = uname().node

LANG = get_value("system_stats")


@register(outgoing=True, pattern="^.alive$")
async def amialive(e):
    me = await e.client.get_me()
    if isinstance(PLUGIN_MESAJLAR['alive'], str):
        await e.edit(PLUGIN_MESAJLAR['alive'].format(
            telethon=version.__version__,
            python=python_version(),
            neon=NEON_VERSION,
            plugin=len(CMD_HELP),
            id=me.id,
            username='@' + me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
            first_name=me.first_name,
            last_name=me.last_name if me.last_name else '',
            mention=f'[{me.first_name}](tg://user?id={me.id})'
        ))
    else:
        await e.delete()
        if not PLUGIN_MESAJLAR['alive'].text == '':
            PLUGIN_MESAJLAR['alive'].text = PLUGIN_MESAJLAR['alive'].text.format(
                telethon=version.__version__,
                python=python_version(),
                neon=NEON_VERSION,
                plugin=len(CMD_HELP),
                id=me.id,
                username='@' +
                me.username if me.username else f'[{me.first_name}](tg://user?id={me.id})',
                first_name=me.first_name,
                last_name=me.last_name if me.last_name else '',
                mention=f'[{me.first_name}](tg://user?id={me.id})')
        if e.is_reply:
            await e.respond(PLUGIN_MESAJLAR['alive'], reply_to=e.message.reply_to_msg_id)
        else:
            await e.respond(PLUGIN_MESAJLAR['alive'])


@register(incoming=True, from_users=WHITELIST, pattern="^.live$")
@register(incoming=True, from_users=yetimler, pattern="^.live$")
async def ownerlive(owner):
    if owner.fwd_from:
        return
    if owner.is_reply:
        reply = await owner.get_reply_message()
        reply.text
        reply_user = await owner.client.get_entity(reply.from_id)
        ren = reply_user.id
        if owner.sender_id == WHITELIST:
            bat = "Ətağa"
        else:
            bat = "Ətağa"
        if ren == nusrte:
            str(NEON_VERSION.replace("v", ""))
            await owner.reply(f"**{bat}** **N Σ O N aktivdir...**\n**Version:** `{NEON_VERSION}` 🪄")
        else:
            return
    else:
        return

CmdHelp("alive").add_command(
    "alive", None, "N Σ O N'un fəaliyyətini yoxlamaq üçündür."
).add()
