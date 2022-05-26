from telethon import events
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from time import sleep as t
from userbot import bot
import telethon


@register(outgoing=True, pattern="^.bass(?: |$)(.*)")
async def BassBooster(event):
    if event.fwd_from:
        return
    if event.pattern_match.group(1):
        input = event.pattern_match.group(1)
    else:
        await event.edit("🔸 __Bass effekti üçün bass səviyyəsi təyin et!__")
        return
    if not event.reply_to_msg_id:
        await event.edit("ℹ️ __Hansı musiqiyə bass vermək lazımdırsa, cavab ver ona.__")
        return
    cavab = await event.get_reply_message()
    if not cavab.media:
        await event.edit("ℹ️ __Hansı musiqiyə bass vermək lazımdırsa, cavab ver ona.__")
        return
    me = await event.client.get_me()
    username = f"@{me.username}" if me.username else my_mention
    chat = "@Baasss_bot"
    await event.edit("__Bass effekti gücləndirilir...__ 🔊")
    await bot(telethon.tl.functions.contacts.UnblockRequest(chat))
    async with event.client.conversation(chat) as conv:
        response = conv.wait_event(events.NewMessage(incoming=True,from_users=488701812))
        reply = await event.client.send_message(chat, cavab)
        t(3)
        strr = await event.client.send_message(chat,input)
        responsee = await response
        response = responsee.message.media
        await event.client.send_file(event.chat_id, response,
                caption="""
<b>🔸 Bass səviyyəsi <a href=\"https://t.me/Neonsup\">N Σ O N</a> ilə gücləndirildi.
🔊 Bass səviyyəsi -</b> <code>{}</code>
🀄️ <b>Mənim Sahibim - {}</b>
""".format(input, username), parse_mode="HTML", reply_to=cavab)
        await event.client.send_read_acknowledge(conv.chat_id)
        await event.delete()

# ------------------------------ CMDHELP ------------------------------------

Kömək = CmdHelp('bass')
Kömək.add_command("bass <Audio faylına cavab>", "<Bass səviyyəsi>", "Musiqinin bass səviyyəsini çoxaldar.")
Kömək.add_info("**@Xwarn | @NeonDevs.**")
Kömək.add()
