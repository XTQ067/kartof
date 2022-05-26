
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.events import register
from userbot.cmdhelp import CmdHelp
from userbot import bot


@register(outgoing=True, pattern="^.download ?(.*)")
@register(outgoing=True, pattern="^.endir ?(.*)")
async def neoninsta(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Yükləmək üçün bir linki yanıtlayın.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("`Yükləmək üçün bir linki yanıtlayın.`")
        return
    chat = "@SaveAsbot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("Sender istifadəçini tapmadığı üçün script dayandırıldı.")
        return
    await event.edit("`Yüklənir...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=523131145)
            )
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.edit(" @SaveAsBot `blokdan çıxardın və bir daha yenidən yoxlayın`")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "Gizlilik ayarlarınızdakı ileti qismini düzəldin."
            )
        else:
            await event.delete()
            await event.client.send_file(
                event.chat_id,
                response.message.media,
                caption=f"`@NeonUserBot ilə yükləndi`",
            )
            await event.client.send_read_acknowledge(conv.chat_id)


Help = CmdHelp('download')
Help.add_command('download və ya .endir', '<link/cavab>', 'Instagram, tiktok, pinterestdən post yükləyər.')
Help.add()
