from userbot.events import register
from userbot.cmdhelp import CmdHelp
from PIL import Image
import os

@register(outgoing=True, pattern=".size$")
async def size(e):
    r = await e.get_reply_message()
    if not (r and r.media):
        return await e.edit("şəkilə yaxud stikerə cavab ver.")
    if hasattr(r.media, "document"):
        img = await e.client.download_media(r, thumb=-1)
    else:
        img = await r.download_media()
    im = Image.open(img)
    x, y = im.size
    await e.edit(f"Bu şəklin ölçüsü:\n`{x} x {y}`")
    os.remove(img)

Help = CmdHelp("segment")
Help.add_command("size", "<cavab>", "Görüntünün ölçüsünü qeyd edər.")
Help.add()
