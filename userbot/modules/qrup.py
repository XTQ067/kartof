from userbot.events import register
import asyncio
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from userbot.cmdhelp import CmdHelp


@register(outgoing=True,
          pattern="^.banall"
          )
async def banall(event):
    await event.edit("**İstifadəçilər qrupdan çıxarılır...**")
    ben = await event.client.get_me()
    all_participants = await event.client.get_participants(event.chat_id)
    for user in all_participants:
        if user.id == ben.id:
            pass
        try:
            await event.client(EditBannedRequest(
                event.chat_id, int(user.id), ChatBannedRights(
                    until_date=None,
                    view_messages=True
                )
            ))
        except Exception as e:
            await event.reply(str(e))
        await asyncio.sleep(0.3)
    await event.edit("**:D**")

Help = CmdHelp('bannall')
Help.add_command(
    'banall',
    None,
    'Admin olduğunuz hər hansısa qrupdakı istfadəçilərin hamısını ban edər.')
Help.add_info('@YarasaBots heyyəti məsuliyyət daışımır. Diqqətli olun!')
Help.add()
