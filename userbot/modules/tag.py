from telethon.tl import types
import re, asyncio, random, telethon, sys, os
from telethon.tl.types import *
from userbot.cmdhelp import CmdHelp
from userbot.events import register
from userbot.text import emoji
from time import sleep as t
from userbot import bot
from userbot.main import PLUGIN_MESAJLAR

# ---------------------------------------------------------------------------

@register(pattern="^.tag(?: |$)(.*)", outgoing=True, groups_only=True)
async def tagger(q):
    if q.fwd_from:
        return

    if q.pattern_match.group(1):
        s = q.pattern_match.group(1)
    else:

        c = await q.get_input_chat()
        a_ = 0
        await q.delete()
        async for i in bot.iter_participants(c):
          if a_ == 5000:
            break
          a_ += 1
          await q.client.send_message(q.chat_id, "[{}](tg://user?id={}) {}".format(i.first_name, i.id, s))
          t(1.5)

# --------------------------------------------------------------------------------------------------------------------------------

@register(outgoing=True, pattern="^.admins$", groups_only=True)
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "Bu qrupda"
    mentions = f'<b>{title} admin siyahısı:</b> \n'
    try:
        async for user in show.client.iter_participants(show.chat_id, filter=ChannelParticipantsAdmins):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nDeleted Account <code>{user.id}</code>"
    except telethon.errors.ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")
      
        

@register(outgoing=True, pattern="^.bots$", groups_only=True)
async def get_bots(show):
    """ .bots  """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f'<b> {title} qrupunda tapılan botlar:</b>\n'
    try:
       # if isinstance(message.to_id, PeerChat):
        #    await show.edit("`Sadəcə super qrupların botlara sahib ola biləcəyini eşitdim.`")
        #   return
       # else:
        async for user in show.client.iter_participants(
                show.chat_id, filter=ChannelParticipantsBots):
            if not user.deleted:
                link = f"<a href=\"tg://user?id={user.id}\">{user.first_name}</a>"
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nSilinmiş bot <code>{user.id}</code>"
    except telethon.errors.ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions, parse_mode="html")
    except telethon.errors.rpcerrorlist.MessageTooLongError:
        await show.edit("**Lənət olsun, burda çox bot var. Botların listini fayl olaraq göndərirəm.**")
        file = open("botlist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "botlist.txt",
            caption='{} qrubunda tapılam botlar:'.format(title),
            reply_to=show.id,
        )
        os.remove("botlist.txt")
# ---------------------------------------------------------------------------------------------------------------


usernexp = re.compile(r"@(\w{3,32})\[(.+?)\]")
nameexp = re.compile(r"\[([\w\S]+)\]\(tg://user\?id=(\d+)\)\[(.+?)\]")


@register(outgoing=True, ignore_unsafe=True, disable_errors=True)
async def mention(event):
    newstr = event.text
    if event.entities:
        newstr = nameexp.sub(r'<a href="tg://user?id=\2">\3</a>', newstr, 0)
        for match in usernexp.finditer(newstr):
            user = match.group(1)
            text = match.group(2)
            name, entities = await bot._parse_message_text(text, "md")
            rep = f'<a href="tg://resolve?domain={user}">{name}</a>'
            if entities:
                for e in entities:
                    tag = None
                    if isinstance(e, types.MessageEntityBold):
                        tag = "<b>{}</b>"
                    elif isinstance(e, types.MessageEntityItalic):
                        tag = "<i>{}</i>"
                    elif isinstance(e, types.MessageEntityCode):
                        tag = "<code>{}</code>"
                    elif isinstance(e, types.MessageEntityStrike):
                        tag = "<s>{}</s>"
                    elif isinstance(e, types.MessageEntityPre):
                        tag = "<pre>{}</pre>"
                    elif isinstance(e, types.MessageEntityUnderline):
                        tag = "<u>{}</u>"
                    if tag:
                        rep = tag.format(rep)
            newstr = re.sub(re.escape(match.group(0)), rep, newstr)
    if newstr != event.text:
        await event.edit(newstr, parse_mode="html")

# ------------------------------------------------------------------------------------------


class FlagContainer:
    is_active = False


@register(pattern=r"^\.etag(?: |$)(.*)", outgoing=True, groups_only=True)
async def b(event):
    if event.fwd_from or FlagContainer.is_active:
        return
    try:
        FlagContainer.is_active = True

        text = None
        args = event.message.text.split(" ", 1)
        if len(args) > 1:
            text = args[1]

        chat = await event.get_input_chat()
        await event.delete()

        tags = list(map(lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})", await event.client.get_participants(chat)))
        current_pack = []
        async for participant in event.client.iter_participants(chat):
            if not FlagContainer.is_active:
                break

            current_pack.append(participant)

            if len(current_pack) == 5:
                tags = list(
                    map(lambda m: f"[{random.choice(emoji)}](tg://user?id={m.id})", current_pack))
                current_pack = []

                if text:
                    tags.append(text)

                await event.client.send_message(event.chat_id, " ".join(tags))
                t(1.5)
    finally:
        FlagContainer.is_active = False


@register(outgoing=True, pattern="^.tagstop$")
async def restart(event):
    await event.edit(PLUGIN_MESAJLAR['tagstop'])

    try:
        await bot.disconnect()
    except BaseException:
        pass
    
    os.execl(sys.executable, sys.executable, *sys.argv)

# ------------------------------ CMDHELP --------------------------------------

Help = CmdHelp("tag")
Help.add_command("tag", "<səbəb>","Qrupdakı şəxsləri tag edər.")
Help.add_command("admins", None,"Qrupdakı adminləri tag edər")
Help.add_command('etag','<səbəb>','Qrupdakı şəxsləri fərqli emojilərlə tag edər.')
Help.add_command('bots', None, "Qrupdakı botları bir mesajda tag edər.")
Help.add_command('@tag[istədiyiniz ad/söz]','İnsanlanları istədiyiniz kimi tag edin','Əvvəlində nöqtə qoymadan işlədin. Nümunə: @NeonUserBot[N Σ O N]')
Help.add_command('tagstop', None, "Qrupdakı botları bir mesajda tag edər.")
Help.add()
