from telethon.errors import ChannelInvalidError, ChannelPrivateError, ChannelPublicGroupNaError
from emoji import emojize
from telethon.tl.types import MessageActionChannelMigrateFrom, ChannelParticipantsAdmins
from telethon.tl.functions.messages import GetHistoryRequest, GetFullChatRequest
from userbot.events import register
from datetime import datetime
from math import sqrt
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.utils import get_input_location
from userbot.cmdhelp import CmdHelp
from telethon.errors import (ChatAdminRequiredError, UserAdminInvalidError)
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (ChannelParticipantsAdmins, ChatBannedRights)
import asyncio, telethon
from time import sleep
from userbot import BOTLOG, BOTLOG_CHATID, bot
from userbot.language import get_value

from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto, ChannelParticipantsBots,
                               User)

from telethon.errors import (ChatAdminRequiredError, ImageProcessFailedError,
                             PhotoCropSizeSmallError, UserAdminInvalidError)

dil = get_value("admin")

PP_TOO_SMOL = dil['PP_TOO_SMOL']
PP_ERROR = dil['PP_ERROR']
NO_ADMIN = dil['NO_ADMIN']
NO_PERM = dil['NO_PERM']
NO_SQL = dil['NO_SQL']

CHAT_PP_CHANGED = dil['CHAT_PP_CHANGED']
CHAT_PP_ERROR = dil['CHAT_PP_ERROR']
INVALID_MEDIA = dil['INVALID_MEDIA']

@register(outgoing=True,pattern="^.qrupinfo(?: |$)(.*)")
async def info(event):
    await event.edit("`Qrup analiz edilir...`")
    chat = await get_chatinfo(event)
    caption = await fetch_info(chat, event)
    try:
        await event.edit(caption, parse_mode="html")
    except Exception as e:
        print("Exception:", e)
        await event.edit("`Gözlənilməz bir xəta baş verdi.`")
    return


async def get_chatinfo(event):
    chat = event.pattern_match.group(1)
    chat_info = None
    if chat:
        try:
            chat = int(chat)
        except ValueError:
            pass
    if not chat:
        if event.reply_to_msg_id:
            replied_msg = await event.get_reply_message()
            if replied_msg.fwd_from and replied_msg.fwd_from.channel_id is not None:
                chat = replied_msg.fwd_from.channel_id
        else:
            chat = event.chat_id
    try:
        chat_info = await event.client(GetFullChatRequest(chat))
    except BaseException:
        try:
            chat_info = await event.client(GetFullChannelRequest(chat))
        except ChannelInvalidError:
            await event.reply("`Keçərsiz kanal/qrup`")
            return None
        except ChannelPrivateError:
            await event.reply("`Bura gizli qrupdur vəya mən burdan banlanmışam.`")
            return None
        except ChannelPublicGroupNaError:
            await event.reply("`Belə bir qrup vəya kanal yoxdur`")
            return None
        except (TypeError, ValueError) as err:
            await event.reply(str(err))
            return None
    return chat_info


async def fetch_info(chat, event):
    # chat.chats is a list so we use get_entity() to avoid IndexError
    chat_obj_info = await event.client.get_entity(chat.full_chat.id)
    broadcast = chat_obj_info.broadcast if hasattr(
        chat_obj_info, "broadcast") else False
    chat_type = "Channel" if broadcast else "Group"
    chat_title = chat_obj_info.title
    warn_emoji = emojize(":warning:")
    try:
        msg_info = await event.client(GetHistoryRequest(peer=chat_obj_info.id, offset_id=0, offset_date=datetime(2010, 1, 1),
                                                        add_offset=-1, limit=1, max_id=0, min_id=0, hash=0))
    except Exception as e:
        msg_info = None
        print("Exception:", e)
    # No chance for IndexError as it checks for msg_info.messages first
    first_msg_valid = True if msg_info and msg_info.messages and msg_info.messages[
        0].id == 1 else False
    # Same for msg_info.users
    creator_valid = True if first_msg_valid and msg_info.users else False
    creator_id = msg_info.users[0].id if creator_valid else None
    creator_firstname = msg_info.users[0].first_name if creator_valid and msg_info.users[
        0].first_name is not None else "Deleted Account"
    creator_username = msg_info.users[0].username if creator_valid and msg_info.users[0].username is not None else None
    created = msg_info.messages[0].date if first_msg_valid else None
    former_title = msg_info.messages[0].action.title if first_msg_valid and isinstance(
        msg_info.messages[0].action,
        MessageActionChannelMigrateFrom) and msg_info.messages[0].action.title != chat_title else None
    try:
        dc_id, location = get_input_location(chat.full_chat.chat_photo)
    except Exception as e:
        dc_id = "Unknown"
        str(e)

    # this is some spaghetti I need to change
    description = chat.full_chat.about
    members = chat.full_chat.participants_count if hasattr(
        chat.full_chat, "participants_count") else chat_obj_info.participants_count
    admins = chat.full_chat.admins_count if hasattr(
        chat.full_chat, "admins_count") else None
    banned_users = chat.full_chat.kicked_count if hasattr(
        chat.full_chat, "kicked_count") else None
    restrcited_users = chat.full_chat.banned_count if hasattr(
        chat.full_chat, "banned_count") else None
    members_online = chat.full_chat.online_count if hasattr(
        chat.full_chat, "online_count") else 0
    group_stickers = chat.full_chat.stickerset.title if hasattr(
        chat.full_chat, "stickerset") and chat.full_chat.stickerset else None
    messages_viewable = msg_info.count if msg_info else None
    messages_sent = chat.full_chat.read_inbox_max_id if hasattr(
        chat.full_chat, "read_inbox_max_id") else None
    messages_sent_alt = chat.full_chat.read_outbox_max_id if hasattr(
        chat.full_chat, "read_outbox_max_id") else None
    exp_count = chat.full_chat.pts if hasattr(chat.full_chat, "pts") else None
    username = chat_obj_info.username if hasattr(
        chat_obj_info, "username") else None
    bots_list = chat.full_chat.bot_info  # this is a list
    bots = 0
    supergroup = "<b>Evet</b>" if hasattr(chat_obj_info,
                                          "megagroup") and chat_obj_info.megagroup else "No"
    slowmode = "<b>Evet</b>" if hasattr(chat_obj_info,
                                        "slowmode_enabled") and chat_obj_info.slowmode_enabled else "No"
    slowmode_time = chat.full_chat.slowmode_seconds if hasattr(
        chat_obj_info, "slowmode_enabled") and chat_obj_info.slowmode_enabled else None
    restricted = "<b>Evet</b>" if hasattr(chat_obj_info,
                                          "restricted") and chat_obj_info.restricted else "No"
    verified = "<b>Evet</b>" if hasattr(chat_obj_info,
                                        "verified") and chat_obj_info.verified else "No"
    username = "@{}".format(username) if username else None
    creator_username = "@{}".format(
        creator_username) if creator_username else None
    # end of spaghetti block

    if admins is None:
        # use this alternative way if chat.full_chat.admins_count is None,
        # works even without being an admin
        try:
            participants_admins = await event.client(GetParticipantsRequest(channel=chat.full_chat.id, filter=ChannelParticipantsAdmins(),
                                                                            offset=0, limit=0, hash=0))
            admins = participants_admins.count if participants_admins else None
        except Exception as e:
            print("Exception:", e)
    if bots_list:
        for bot in bots_list:
            bots += 1

    caption = "<b>Qrup bilgisi:</b>\n"
    caption += f"ID: <code>{chat_obj_info.id}</code>\n"
    if chat_title is not None:
        caption += f"{chat_type} adı: {chat_title}\n"
    if former_title is not None:  # Meant is the very first title
        caption += f"Köhnə adı {former_title}\n"
    if username is not None:
        caption += f"{chat_type} növü: Açıq\n"
        caption += f"Link: {username}\n"
    else:
        caption += f"{chat_type} Növü: Gizli\n"
    if creator_username is not None:
        caption += f"Sahib: {creator_username}\n"
    elif creator_valid:
        caption += f"Sahib: <a href=\"tg://user?id={creator_id}\">{creator_firstname}</a>\n"
    if created is not None:
        caption += f"Qurulma Tarixi: <code>{created.date().strftime('%b %d, %Y')} - {created.time()}</code>\n"
    else:
        caption += f"Qurulma Tarixi: <code>{chat_obj_info.date.date().strftime('%b %d, %Y')} - {chat_obj_info.date.time()}</code> {warn_emoji}\n"
    caption += f"Məlumat Mərkəzi ID: {dc_id}\n"
    if exp_count is not None:
        chat_level = int((1 + sqrt(1 + 7 * exp_count / 14)) / 2)
        caption += f"{chat_type} seviyesi: <code>{chat_level}</code>\n"
    if messages_viewable is not None:
        caption += f"Görünən mesajlar: <code>{messages_viewable}</code>\n"
    if messages_sent:
        caption += f"Göndərilən mesajlar: <code>{messages_sent}</code>\n"
    elif messages_sent_alt:
        caption += f"Göndərilən mesajlar: <code>{messages_sent_alt}</code> {warn_emoji}\n"
    if members is not None:
        caption += f"İsdifadəçilər: <code>{members}</code>\n"
    if admins is not None:
        caption += f"Adminlər: <code>{admins}</code>\n"
    if bots_list:
        caption += f"Botlar: <code>{bots}</code>\n"
    if members_online:
        caption += f"Hal Hazırda Aktiv: <code>{members_online}</code>\n"
    if restrcited_users is not None:
        caption += f"Məhdud İsdifadəçilər: <code>{restrcited_users}</code>\n"
    if banned_users is not None:
        caption += f"Banlanan İsdifadəçilər: <code>{banned_users}</code>\n"
    if group_stickers is not None:
        caption += f"{chat_type} Stickerləri: <a href=\"t.me/addstickers/{chat.full_chat.stickerset.short_name}\">{group_stickers}</a>\n"
    caption += "\n"
    if not broadcast:
        caption += f"Yavaş mod: {slowmode}"
        if hasattr(
                chat_obj_info,
                "slowmode_enabled") and chat_obj_info.slowmode_enabled:
            caption += f", <code>{slowmode_time}s</code>\n\n"
        else:
            caption += "\n\n"
    if not broadcast:
        caption += f"Supergroup: {supergroup}\n\n"
    if hasattr(chat_obj_info, "restricted"):
        caption += f"Məhdudlanan: {restricted}\n"
        if chat_obj_info.restricted:
            caption += f"> Platforma: {chat_obj_info.restriction_reason[0].platform}\n"
            caption += f"> Səbəb: {chat_obj_info.restriction_reason[0].reason}\n"
            caption += f"> Yazı: {chat_obj_info.restriction_reason[0].text}\n\n"
        else:
            caption += "\n"
    if hasattr(chat_obj_info, "scam") and chat_obj_info.scam:
        caption += "Scam: <b>Evet</b>\n\n"
    if hasattr(chat_obj_info, "verified"):
        caption += f"Telegram tərəfindən doğrulandı: {verified}\n\n"
    if description:
        caption += f"Açıqlama: \n<code>{description}</code>\n"
    return caption
# ---------------------------------------------------------------------------------------------------

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

# ------------------------------------------------------------------------------------------------------


@register(pattern="^.zombies(?: |$)(.*)",outgoing=True, groups_only=True)
async def delete_accounts_cleaner(e):
    command_input = e.pattern_match.group(1).lower()
    say = 0
    silinmə = "**Qrupda silinmiş hesab tapmadım. Bu qrup təmizdir.**"

    # ikinci emr. tapilan silinmis hesablari siler.
    if command_input != "clean":
        await e.edit(f"<b>{e.chat.title} qrupunda silinmiş hesabları axtarıram...</b>", parse_mode="HTML")
        async for user in e.client.iter_participants(e.chat_id):
            if user.deleted:
                say += 1
                await asyncio.sleep(1)
        if say > 0:
            silinmə = f"**{say}** nəfər silinmiş hesab tapdım."
        await e.edit(silinmə)
        return

    chat = await e.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    # Əgər admin və ya qurucu deyilsə nə etsin
    if not admin and not creator:
        await e.edit(f"**Sənin {e.chat.title} qrupunda adminliyin yoxdur.**")
        return
    await e.edit("**Silinmiş hesablar çıxarılır...**")
    say = 0
    del_a = 0

    async for user in e.client.iter_participants(e.chat_id):
        if user.deleted:
            try:
                await e.client(
                    EditBannedRequest(e.chat_id, user.id, BANNED_RIGHTS))
            except ChatAdminRequiredError:
                await e.edit("Sənin istifadəçiləri qadağan etmək üçün yetkin yoxdur.")
                return
            except UserAdminInvalidError:
                say -= 1
                del_a += 1
            await e.client(
                EditBannedRequest(e.chat_id, user.id, UNBAN_RIGHTS))
            say += 1

    if say > 0:
        silinmə = f"**{say}** ```ədəd silinmiş hesab çıxarıldı.```"

    if del_a > 0:
        silinmə = f"""**{say}** ```ədəd silinmiş hesab çıxarıldı.```
**{del_a}** ```admin hesabı olduğu üçün çıxara bilmədim. (Ancaq qrupun sahibi çıxara bilər).```"""

    await e.edit(silinmə)
    await asyncio.sleep(2)
    await e.delete()

    if BOTLOG:
        await bot.send_message(
            BOTLOG_CHATID,
            f"""
<b>#TƏMİZLİK</b>
<code>Təmizlik zamanı</code> <b>{say}</b> <code>silinmiş hesab qrupdan çıxarıldı.</code>
<b>QRUPUN ADI:</b> <code>{e.chat.title}</code>
<b>QRUP İD'İ:</b> <code>{e.chat_id}</code>

<b>@NeonUserBot 🎴</b>
""", parse_mode="HTML")


@register(outgoing=True, pattern="^.getlink", groups_only=True)
async def _(event):
    await event.edit("Hazırlanır...")
    try:
        e = await event.client(telethon.tl.functions.messages.ExportChatInviteRequest(event.chat_id))
    except telethon.errors.ChatAdminRequiredError:
        return await event.edit(dil['NO_ADMIN'])
        sleep(7)
        await event.delete()
    await event.edit(f"**Link:** `{e.link}`")


@register(outgoing=True, pattern="^.setgpic$")
async def set_group_photo(gpic):
    """ .setgpic """
    if not gpic.is_group:
        await gpic.edit(dil['PRIVATE'])
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None

    if not admin and not creator:
        await gpic.edit(NO_ADMIN)
        return

    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split('/'):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            await gpic.edit(INVALID_MEDIA)

    if photo:
        try:
            await gpic.client(telethon.tl.functions.channels.EditPhotoRequest(gpic.chat_id, await
                                 gpic.client.upload_file(photo)))
            await gpic.edit(CHAT_PP_CHANGED)

        except PhotoCropSizeSmallError:
            await gpic.edit(PP_TOO_SMOL)
        except ImageProcessFailedError:
            await gpic.edit(PP_ERROR)


Help = CmdHelp('chataction')
Help.add_command('chatinfo', None, 'Qrup haqqında məlumat verər.')
Help.add_command("zombies",None,"Qrupda olan silinmiş hesabları müəyyən etmək üçün əmr.")
Help.add_command("zombies clean",None,"Qrupda olan silinmiş hesabları tapıb silər.")
Help.add_command('getlink', None, 'Qrup linkini verər')
Help.add_command('setgpic', "<cavablama>", "Qrup fotosunu dəyişdirər.")
Help.add()
