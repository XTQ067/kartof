
import os
from userbot import bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp


@register(outgoing=True, pattern="^.bax|^.oxu|^.rr")
async def _(event):
    b = await event.client.download_media(await event.get_reply_message())
    a = open(b, "r")
    c = a.read()
    a.close()
    a = await event.edit("📃 **Faylı açıram...**")
    if len(c) > 4095:
        await a.edit(
            "❌**XƏTA** \n**Telegram** `4095` **mesaj limitinə icazə verir.** \n❗**Limit aşıldığı üçün proses ləğv olundu**"
        )
    else:
        await event.client.send_message(event.chat_id, f"```{c}```")
        await a.delete()
    os.remove(b)


@register(
    pattern="^.ttf|^.pack|^.py",
    outgoing=True,
)
async def TextToFile(e):
    ad = e.text[5:]
    yanit = await e.get_reply_message()
    if yanit.text:
        with open(ad, "w") as fayl:
            fayl.write(yanit.message)
        await e.delete()
        await bot.send_file(e.chat_id,
                            ad,
                            force_document=True)
        os.remove(ad)
        return

CmdHelp('tool').add_command(
    'bax',
    'Bir fayla cavab olaraq yazın.',
    'Faylın məzmununu göstərər.').add_command(
        'ttf',
        'Bir mətnə cavab olaraq yazın.',
    'Cavab verdiyiniz mətni yazdığınız ad ilə istədiyiniz fayl növünə çevirər.').add()
