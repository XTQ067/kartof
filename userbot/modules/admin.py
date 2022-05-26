from telethon.tl.functions.channels import EditAdminRequest ,EditBannedRequest, InviteToChannelRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights, MessageEntityMentionName, User
from userbot import BOTLOG, BOTLOG_CHATID, BRAIN_CHECKER, WARN_LIMIT, WARN_MODE, WHITELIST
from telethon.tl.functions.messages import UpdatePinnedMessageRequest, AddChatUserRequest
from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.errors.rpcerrorlist import MessageTooLongError
from userbot.main import PLUGIN_MESAJLAR
from userbot.language import get_value
from userbot.cmdhelp import CmdHelp
from userbot.events import register
from asyncio import sleep
from userbot import bot 
from os import remove
import datetime
import telethon

# Language 
LANG = get_value("admin")

# --
PP_TOO_SMOL = LANG['PP_TOO_SMOL']
PP_ERROR = LANG['PP_ERROR']
NO_ADMIN = LANG['NO_ADMIN']
NO_PERM = LANG['NO_PERM']
NO_SQL = LANG['NO_SQL']

CHAT_PP_CHANGED = LANG['CHAT_PP_CHANGED']
CHAT_PP_ERROR = LANG['CHAT_PP_ERROR']
INVALID_MEDIA = LANG['INVALID_MEDIA']

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
# ================================================


@register(outgoing=True, pattern="^.add ?(.*)")
async def elave(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("Bu istifadəçini gizlikik səbəbindən qruplara əlavə etmək olmur.")
    else:
        if not event.is_channel and event.is_group:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} qrupa əlavə edilir...`')
                try:
                    await event.client(AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=1000000
                    ))
                except Exception:
                    await event.edit(f'`{user_id} qrupa əlavə edilmədi!`')
                    continue
                await event.edit(f'`{user_id} qrupa edildi!`')
        else:
            for user_id in to_add_users.split(" "):
                await event.edit(f'`{user_id} qrupa əlavə edilir...`')
                try:
                    await event.client(InviteToChannelRequest(
                        channel=event.chat_id,
                        users=[user_id]
                    ))
                except Exception:
                    await event.edit(f'`{user_id} qrupa əlavə edilmədi!`')
                    continue
                await event.edit(f'`{user_id} qrupa əlavə edildi!`')


@register(outgoing=True, pattern="^.gban(?: |$)(.*)")
# @register(incoming=True, from_users=SUDO_ID, pattern="^.gban(?: |$)(.*)")
async def gbanspider(gspdr):
    """ .gban  """
    #
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    #
    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except BaseException:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    #
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    # .
    await gspdr.edit(LANG['BANNING'])
    if gban(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GBANNED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GBANNED_REASON']} {reason}")
        else:
            await gspdr.edit(LANG['GBANNED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")


@register(incoming=True)
async def gbanmsg(moot):
    """ """
    try:
        from userbot.modules.sql_helper.gban_sql import is_gbanned
    except BaseException:
        return

    gbanned = is_gbanned(str(moot.sender_id))
    if gbanned == str(moot.sender_id):
        try:
            chat = await moot.get_chat()
        except BaseException:
            return

        if (isinstance(chat, User)):
            return

        admin = chat.admin_rights
        creator = chat.creator

        if not admin and not creator:
            return

        try:
            await moot.client(EditBannedRequest(moot.chat_id, moot.sender_id,
                                                BANNED_RIGHTS))
            await moot.reply(LANG['GBAN_TEXT'])
        except BaseException:
            return


@register(outgoing=True, pattern="^.ungban(?: |$)(.*)")
async def ungban(un_gban):
    """ .ungban  """
    #
    chat = await un_gban.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await un_gban.edit(NO_ADMIN)
        return

    #
    try:
        from userbot.modules.sql_helper.gban_sql import ungban
    except BaseException:
        await un_gban.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gban)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gban.edit(LANG['UNGBANNING'])

    if ungban(user.id) is False:
        await un_gban.edit(LANG['NO_BANNED'])
    else:
        #
        await un_gban.edit(LANG['UNGBANNED'])

        if BOTLOG:
            await un_gban.client.send_message(
                BOTLOG_CHATID, "#UNGBAN\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gban.chat.title}(`{un_gban.chat_id}`)")


@register(outgoing=True, pattern="^.promote(?: |$)(.*)")
@register(incoming=True, from_users=BRAIN_CHECKER,
          pattern="^.promote(?: |$)(.*)")
# @register(incoming=True, from_users=SUDO_ID, pattern="^.promote(?: |$)(.*)")
async def promote(promt):
    """ .promote """
    #
    chat = await promt.get_chat()
    #
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await promt.edit(NO_ADMIN)
        return

    new_rights = ChatAdminRights(add_admins=True,
                                 invite_users=True,
                                 change_info=True,
                                 ban_users=True,
                                 delete_messages=True,
                                 pin_messages=True)

    await promt.edit(LANG['PROMOTING'])
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "Admin"  #

    if user:
        pass
    else:
        return

    #
    try:
        await promt.client(
            EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await promt.edit(LANG['SUCCESS_PROMOTE'])

    #
    #
    except BaseException:
        await promt.edit(NO_PERM)
        return

    #
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID, "#ADMİNLİK\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {promt.chat.title}(`{promt.chat_id}`)")


@register(outgoing=True, pattern="^.demote(?: |$)(.*)")
@register(incoming=True,
          from_users=BRAIN_CHECKER,
          pattern="^.demote(?: |$)(.*)")
# @register(incoming=True, from_users=SUDO_ID, pattern="^.demote(?: |$)(.*)")
async def demote(dmod):
    """ .demote """
    #
    chat = await dmod.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await dmod.edit(NO_ADMIN)
        return

    #
    await dmod.edit(LANG['UNPROMOTING'])
    rank = "admeme"  #
    user = await get_user_from_event(dmod)
    user = user[0]
    if user:
        pass
    else:
        return

    #
    newrights = ChatAdminRights(add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None)
    #
    try:
        await dmod.client(
            EditAdminRequest(dmod.chat_id, user.id, newrights, rank))

    #
    #
    except BaseException:
        await dmod.edit(NO_PERM)
        return
    await dmod.edit(LANG['UNPROMOTE'])

    #
    if BOTLOG:
        await dmod.client.send_message(
            BOTLOG_CHATID, "#ADMİNLİK_ALMAQ\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {dmod.chat.title}(`{dmod.chat_id}`)")


@register(outgoing=True, pattern="^.ban(?: |$)(.*)")
@register(incoming=True, from_users=BRAIN_CHECKER, pattern="^.ban(?: |$)(.*)")
# @register(incoming=True, from_users=SUDO_ID, pattern="^.ban(?: |$)(.*)")
async def ban(bon):
    """ .ban"""
    #
    chat = await bon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await bon.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(bon)
    if user:
        pass
    else:
        return

    #
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await bon.edit(
            LANG['BRAIN']
        )
        return

    #
    await bon.edit(LANG['BANNING'])

    try:
        await bon.client(EditBannedRequest(bon.chat_id, user.id,
                                           BANNED_RIGHTS))
    except BaseException:
        await bon.edit(NO_PERM)
        return
    #
    try:
        reply = await bon.get_reply_message()
        if reply:
            await reply.delete()
    except BaseException:
        await bon.edit(
            LANG['NO_PERM_BUT_BANNED'])
        return
    #
    #
    SONMESAJ = PLUGIN_MESAJLAR['ban'].format(
        id=user.id,
        username='@' +
        user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
        first_name=user.first_name,
        last_name='' if not user.last_name else user.last_name,
        mention=f"[{user.first_name}](tg://user?id={user.id})",
        date=datetime.datetime.strftime(
            datetime.datetime.now(),
            '%c'),
        count=(
            chat.participants_count -
            1) if chat.participants_count else 'Bilinmiyor')

    if reason:
        await bon.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await bon.edit(SONMESAJ)
    #
    if BOTLOG:
        await bon.client.send_message(
            BOTLOG_CHATID, "#BAN\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {bon.chat.title}(`{bon.chat_id}`)")


@register(outgoing=True, pattern="^.unban(?: |$)(.*)")
# @register(incoming=True, from_users=SUDO_ID, pattern="^.unban(?: |$)(.*)")
async def nothanos(unbon):
    """ .unban """
    #
    chat = await unbon.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unbon.edit(NO_ADMIN)
        return

    #
    await unbon.edit(LANG['UNBANNING'])

    user = await get_user_from_event(unbon)
    user = user[0]
    if user:
        pass
    else:
        return

    try:
        await unbon.client(
            EditBannedRequest(unbon.chat_id, user.id, UNBAN_RIGHTS))
        await unbon.edit(LANG['UNBANNED'].format(
            id=user.id,
            username='@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
            first_name=user.first_name,
            last_name='' if not user.last_name else user.last_name,
            mention=f"[{user.first_name}](tg://user?id={user.id})",
            date=datetime.datetime.strftime(datetime.datetime.now(), '%c'),
            count=(chat.participants_count) if chat.participants_count else 'Bilinmiyor'
        ))

        if BOTLOG:
            await unbon.client.send_message(
                BOTLOG_CHATID, "#UNBAN\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unbon.chat.title}(`{unbon.chat_id}`)")
    except BaseException:
        await unbon.edit(LANG['EXCUSE_ME_WTF'])


@register(outgoing=True, pattern="^.mute(?: |$)(.*)")
# @register(incoming=True, from_users=SUDO_ID, pattern="^.mute(?: |$)(.*)")
async def spider(spdr):
    """
    """
    #
    try:
        from userbot.modules.sql_helper.spam_mute_sql import mute
    except BaseException:
        await spdr.edit(NO_SQL)
        return

    #
    chat = await spdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await spdr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(spdr)
    if user:
        pass
    else:
        return

    #
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await spdr.edit(
            LANG['BRAIN']
        )
        return

    self_user = await spdr.client.get_me()

    if user.id == self_user.id:
        await spdr.edit(
            LANG['NO_MUTE_ME'])
        return

    #
    await spdr.edit(LANG['MUTING'])
    if mute(spdr.chat_id, user.id) is False:
        return await spdr.edit(LANG['ALREADY_MUTED'])
    else:
        try:
            await spdr.client(
                EditBannedRequest(spdr.chat_id, user.id, MUTE_RIGHTS))

            await mutmsg(spdr, user, reason, chat)
        except UserAdminInvalidError:
            await mutmsg(spdr, user, reason, chat)
        except BaseException:
            return await spdr.edit(LANG['WTF_MUTE'])


async def mutmsg(spdr, user, reason, chat):
    #
    SONMESAJ = PLUGIN_MESAJLAR['mute'].format(
        id=user.id,
        username='@' +
        user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
        first_name=user.first_name,
        last_name='' if not user.last_name else user.last_name,
        mention=f"[{user.first_name}](tg://user?id={user.id})",
        date=datetime.datetime.strftime(
            datetime.datetime.now(),
            '%c'),
        count=(
            chat.participants_count) if chat.participants_count else 'Bilinmiyor')

    if reason:
        await spdr.edit(f"{SONMESAJ}\n{LANG['REASON']}: {reason}")
    else:
        await spdr.edit(f"{SONMESAJ}")

    #
    if BOTLOG:
        await spdr.client.send_message(
            BOTLOG_CHATID, "#MUTE\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {spdr.chat.title}(`{spdr.chat_id}`)")


@register(outgoing=True, pattern="^.unmute(?: |$)(.*)")
async def unmoot(unmot):
    #
    chat = await unmot.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    if not admin and not creator:
        await unmot.edit(NO_ADMIN)
        return

    #
    try:
        from userbot.modules.sql_helper.spam_mute_sql import unmute
    except BaseException:
        await unmot.edit(NO_SQL)
        return

    await unmot.edit(LANG['UNMUTING'])
    user = await get_user_from_event(unmot)
    user = user[0]
    if user:
        pass
    else:
        return

    if unmute(unmot.chat_id, user.id) is False:
        return await unmot.edit(LANG['ALREADY_UNMUTED'])
    else:

        try:
            await unmot.client(
                EditBannedRequest(unmot.chat_id, user.id, UNBAN_RIGHTS))
            await unmot.edit(LANG['UNMUTED'].format(
                id=user.id,
                username='@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
                first_name=user.first_name,
                last_name='' if not user.last_name else user.last_name,
                mention=f"[{user.first_name}](tg://user?id={user.id})",
                date=datetime.datetime.strftime(datetime.datetime.now(), '%c'),
                count=(chat.participants_count) if chat.participants_count else 'Bilinmiyor'
            ))
        except UserAdminInvalidError:
            await unmot.edit(LANG['UNMUTED'].format(
                id=user.id,
                username='@' + user.username if user.username else f"[{user.first_name}](tg://user?id={user.id})",
                first_name=user.first_name,
                last_name='' if not user.last_name else user.last_name,
                mention=f"[{user.first_name}](tg://user?id={user.id})",
                date=datetime.datetime.strftime(datetime.datetime.now(), '%c'),
                count=(chat.participants_count) if chat.participants_count else 'Bilinmiyor'
            ))
        except BaseException:
            await unmot.edit(LANG['WTF_MUTE'])
            return

        if BOTLOG:
            await unmot.client.send_message(
                BOTLOG_CHATID, "#UNMUTE\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {unmot.chat.title}(`{unmot.chat_id}`)")


@register(incoming=True)
async def muter(moot):
    """ """
    try:
        from userbot.modules.sql_helper.spam_mute_sql import is_muted
        from userbot.modules.sql_helper.gmute_sql import is_gmuted
    except BaseException:
        return
    muted = is_muted(moot.chat_id)
    gmuted = is_gmuted(moot.sender_id)
    rights = ChatBannedRights(
        until_date=None,
        send_messages=True,
        send_media=True,
        send_stickers=True,
        send_gifs=True,
        send_games=True,
        send_inline=True,
        embed_links=True,
    )
    if muted:
        for i in muted:
            if str(i.sender) == str(moot.sender_id):
                await moot.delete()
                try:
                    await moot.client(
                        EditBannedRequest(moot.chat_id, moot.sender_id, rights))
                except BaseException:
                    pass
    if gmuted:
        for i in gmuted:
            if i.sender == str(moot.sender_id):
                await moot.delete()


@register(outgoing=True, pattern="^.ungmute(?: |$)(.*)")
async def ungmoot(un_gmute):
    """ .ungmute  """
    #
    chat = await un_gmute.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await un_gmute.edit(NO_ADMIN)
        return

    #
    try:
        from userbot.modules.sql_helper.gmute_sql import ungmute
    except BaseException:
        await un_gmute.edit(NO_SQL)
        return

    user = await get_user_from_event(un_gmute)
    user = user[0]
    if user:
        pass
    else:
        return

    await un_gmute.edit(LANG['GUNMUTING'])

    if ungmute(user.id) is False:
        await un_gmute.edit(LANG['NO_GMUTE'])
    else:
        #
        await un_gmute.edit(LANG['UNMUTED'])

        if BOTLOG:
            await un_gmute.client.send_message(
                BOTLOG_CHATID, "#UNGMUTE\n"
                f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
                f"QRUP: {un_gmute.chat.title}(`{un_gmute.chat_id}`)")


@register(outgoing=True, pattern="^.gmute(?: |$)(.*)")
async def gspider(gspdr):
    """ .gmute """
    #
    chat = await gspdr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await gspdr.edit(NO_ADMIN)
        return

    #
    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except BaseException:
        await gspdr.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(gspdr)
    if user:
        pass
    else:
        return

    #
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await gspdr.edit(LANG['BRAIN'])
        return

    #
    await gspdr.edit(LANG['GMUTING'])
    if gmute(user.id) == False:
        await gspdr.edit(
            LANG['ALREADY_GMUTED'])
    else:
        if reason:
            await gspdr.edit(f"{LANG['GMUTED']} {LANG['REASON']}: {reason}")
        else:
            await gspdr.edit(LANG['GMUTED'])

        if BOTLOG:
            await gspdr.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {gspdr.chat.title}(`{gspdr.chat_id}`)")

import os
from userbot.language import get_value
LANG_ = get_value("siyahi")

@register(outgoing=True, pattern="^.list ?(gmute|gban)?")
async def siyahi(event):
    siyahi = event.pattern_match.group(1)
    try:
        if len(siyahi) < 1:
            await event.edit(LANG_['WRONG_INPUT'])
            return
    except BaseException:
        await event.edit(LANG_['WRONG_INPUT'])
        return

    if siyahi == "gban":
        try:
            from userbot.modules.sql_helper.gban_sql import gbanlist
        except BaseException:
            await event.edit(LANG_['NEED_SQL_MODE'])
            return
        await event.edit(LANG_['GBANNED_USERS'])
        mesaj = ""
        for user in gbanlist():
            mesaj += f"**ID: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit(LANG_['TOO_MANY_GBANNED'])
            open("gban_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, LANG_['GBAN_TXT'], file="gban_liste.txt")
            os.remove("gban_liste.txt")
        else:
            await event.edit(LANG_['GBAN_LIST'] % mesaj)
    elif siyahi == "gmute":
        try:
            from userbot.modules.sql_helper.gmute_sql import gmutelist
        except BaseException:
            await event.edit(LANG_['NEED_SQL_MODE'])
            return
        await event.edit(LANG['GMUTE_DATA'])
        mesaj = ""
        for user in gmutelist():
            mesaj += f"**ID: **`{user.sender}`\n"

        if len(mesaj) > 4000:
            await event.edit(LANG_['TOO_MANY_GMUTED'])
            open("gmute_liste.txt", "w+").write(mesaj)
            await event.client.send_message(event.chat_id, LANG_['GMUTE_TXT'], file="gmute_liste.txt")
            os.remove("gmute_liste.txt")
        else:
            await event.edit(LANG_['GMUTE_LIST'] % mesaj)



@register(pattern=".unpin", outgoing=True, groups_only=True)
async def pin(event):    
    if event.reply_to_msg_id:
        msg_id = event.reply_to_msg_id
    else:
        await event.edit(f"**{LANG['MSG_FOR_UNPIN']}**")
        return 

    chat = await event.get_chat()
    try:
        await bot.unpin_message(chat.id, msg_id)
        await event.edit(f"**{LANG['UNPINNED']}**")
        if BOTLOG:
            title = chat.title if chat.title else chat.username if chat.username else chat.id 
            await bot.send_message(BOTLOG_CHATID, f"**#UNPIN\n{LANG['CHAT']}: {title}**")
    except telethon.errors.ChatAdminRequiredError:
        await event.edit(f"**{LANG['NO_ADMIN']}**")
    except Exception as e:
        await event.edit(f"ERROR: {e}")

    return
  
@register(outgoing=True, pattern="^.pin(?: |$)(.*)")
async def pin(msg):
    """ .pin  """
    #
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await msg.edit(NO_ADMIN)
        return

    to_pin = msg.reply_to_msg_id

    if not to_pin:
        await msg.edit(LANG['NEED_MSG'])
        return

    options = msg.pattern_match.group(1)

    is_silent = True

    if options.lower() == "loud":
        is_silent = False

    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BaseException:
        await msg.edit(NO_PERM)
        return

    await msg.edit(LANG['PINNED'])

    user = await get_user_from_id(msg.from_id, msg)

    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID, "#PIN\n"
            f"ADMIN: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {msg.chat.title}(`{msg.chat_id}`)\n"
            f"LOUD: {not is_silent}")


@register(outgoing=True, pattern="^.kick(?: |$)(.*)")
# @register(incoming=True, from_users=SUDO_ID, pattern="^.kick(?: |$)(.*)")
async def kick(usr):
    """ .kick """
    #
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await usr.edit(NO_ADMIN)
        return

    user, reason = await get_user_from_event(usr)
    if not user:
        await usr.edit(LANG['NOT_FOUND'])
        return

    #
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await usr.edit(
            LANG['BRAIN']
        )
        return

    await usr.edit(LANG['KICKING'])

    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(.5)
    except Exception as e:
        await usr.edit(NO_PERM + f"\n{str(e)}")
        return

    if reason:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`\n{LANG['REASON']}: {reason}"
        )
    else:
        await usr.edit(
            f"[{user.first_name}](tg://user?id={user.id}) `{LANG['KICKED']}`")

    if BOTLOG:
        await usr.client.send_message(
            BOTLOG_CHATID, "#KICK\n"
            f"İSTİFADECİ: [{user.first_name}](tg://user?id={user.id})\n"
            f"QRUP: {usr.chat.title}(`{usr.chat_id}`)\n")


@register(outgoing=True, pattern="^.users ?(.*)")
async def get_users(show):
    """ .users """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} QruPunda tapılam istifadəçilər: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinən hesab `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                else:
                    mentions += f"\nSilinən hesab `{user.id}`"
    except Exception as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Lənət olsun, bu böyük bir qrupdur. İstifadəçi listini fayl olaraq göndərirəm.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption='{} qrupundakı istifadəçilər'.format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    """  """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`İstifadəçi adı, ID'sini vəya mesajını yönləndirin!`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj, extra
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj


@register(outgoing=True, pattern="^.unwarn ?(.*)")
async def unwarn(event):
    """ .unwarn """
    #
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    #
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except BaseException:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    #
    await event.edit(LANG['UNWARNING'])
    silme = warn.sil_warn(user.id)
    if not silme:
        await event.edit(LANG['UNWARNED'])
        return

    warnsayi = warn.getir_warn(user.id)

    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {LANG['UNWARN']} {warnsayi}/{WARN_LIMIT}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


@register(outgoing=True, pattern="^.warn ?(.*)")
async def warn(event):
    """ .warn """
    #
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator

    #
    if not admin and not creator:
        await event.edit(NO_ADMIN)
        return

    #
    try:
        import userbot.modules.sql_helper.warn_sql as warn
    except BaseException:
        await event.edit(NO_SQL)
        return

    user, reason = await get_user_from_event(event)
    if user:
        pass
    else:
        return

    #
    if user.id in BRAIN_CHECKER or user.id in WHITELIST:
        await event.edit(LANG['BRAIN'])
        return

    #
    await event.edit(LANG['WARNING'])
    warn.ekle_warn(user.id)
    warnsayi = warn.getir_warn(user.id)
    if warnsayi >= WARN_LIMIT:
        if WARN_MODE == "gban":
            await Warn_Gban(event, warn, user)
        else:
            await Warn_Gmute(event, warn, user)
        return
    await event.edit(f"[{user.first_name}](tg://user?id={user.id})`, {warnsayi}/{WARN_LIMIT} {LANG['WARN']}`")

    if BOTLOG:
        await event.client.send_message(
            BOTLOG_CHATID, "#WARN\n"
            f"USER: [{user.first_name}](tg://user?id={user.id})\n"
            f"CHAT: {event.chat.title}(`{event.chat_id}`)")


async def Warn_Gmute(event, warn, user, reason=None):
    await event.delete()
    yeni = await event.reply(f"`Səni yetəri qədər xəbərdar etdim` [{user.first_name}](tg://user?id={user.id})`, qlobal olaraq susduruldun!`")

    try:
        from userbot.modules.sql_helper.gmute_sql import gmute
    except BaseException:
        await yeni.edit(NO_SQL)
        return

    yeni2 = await yeni.reply("`Susdurulur...`")

    if gmute(user.id) == False:
        await yeni2.edit(
            '`Xəta! İstifadəçi onsuz qlobal olaraq susdurulub.`')
    else:
        if reason is not None:
            await yeni2.edit(f"`İstifadəçi qlobal olaraq susduruldu!`Səbəbi: {reason}")
        else:
            await yeni2.edit("`İstifadəçi qlobal olaraq susduruldu!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GMUTE\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)


async def Warn_Gban(event, warn, user, reason=None):
    await event.delete()
    yeni = await event.reply(f"`Səni yetəri qədər xəbərdar etdim` [{user.first_name}](tg://user?id={user.id})`, qlobal olaraq banlandın!`")

    try:
        from userbot.modules.sql_helper.gban_sql import gban
    except BaseException:
        await yeni.edit(NO_SQL)
        return

    yeni2 = await yeni.reply("`Banlanır...`")

    if gban(user.id) == False:
        await yeni2.edit(
            '`Xəta! İstifadəçi onsuz qlobal olaraq banlanıb.`')
    else:
        if reason is not None:
            await yeni2.edit(f"`İstifadəçi qlobal olaraq banlandı!`Səbəbi: {reason}")
        else:
            await yeni2.edit("`İstifadəçi qlobal olaraq banlandı!`")

        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID, "#GBAN\n"
                f"USER: [{user.first_name}](tg://user?id={user.id})\n"
                f"CHAT: {event.chat.title}(`{event.chat_id}`)")
    warn.toplu_sil_warn(user.id)


@register(outgoing=True, pattern="^.usersdel ?(.*)")
async def get_usersdel(show):
    """ .usersdel  """
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '{} qrupunda tapılman silinməyən hesablar: \n'.format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
    #                mentions += f"\nDeleted Account `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                    show.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    mentions += f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
         #       else:
      #              mentions += f"\nDeleted Account `{user.id}`"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await show.edit(mentions)
    except MessageTooLongError:
        await show.edit(
            "Lənət olsun, bu böyük qrupdur. Silinməyən istifadəçilər listini fayl olaraq göndərirəm.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "deleteduserslist.txt",
            caption='{} qrupuna aid olan silinmiş hesablar:'.format(title),
            reply_to=show.id,
        )
        remove("deleteduserslist.txt")


async def get_userdel_from_event(event):
    """ . """
    args = event.pattern_match.group(1).split(' ', 1)
    extra = None
    if event.reply_to_msg_id and not len(args) == 2:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]

        if user.isnumeric():
            user = int(user)

        if not user:
            await event.edit("`Silinməyən istifadəçinin istifadəçi adını, ID'sini vəya mesajını yönləndirin`")
            return

        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity,
                          MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except Exception as err:
            await event.edit(str(err))
            return None

    return user_obj, extra


async def get_userdel_from_id(user, event):
    if isinstance(user, str):
        user = int(user)

    try:
        user_obj = await event.client.get_entity(user)
    except Exception as err:
        await event.edit(str(err))
        return None

    return user_obj

#

Help = CmdHelp('admin')
Help.add_command('promote', "<istifadəçi adı/cavablama> <özəl ad (istəyə bağlı)>", "Söhbətdəki istifadəçiyə idarəçi haqqları verir.")
Help.add_command('demote', "<istifadəçi adı/cavablama>", "Söhbətdəki istifadəçinin idarəçi icazələrini ləğv edər.")
Help.add_command('ban', "<istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>", "Söhbətdəki istifadəçini banlayar.")
Help.add_command('unban', "<istifadəçi adı/cavablama>", "Söhbətdəki istifadəçinin bandan çıxardar.")
Help.add_command('warn', "<istifadəçi adı/cavablamma> <səbəb (istəyə bağlı>", "Seçdiyiniz istifadəçiyi xəbərdar edər.")
Help.add_command('unwarn', "<istifadəçi adı/cavablamma>", "Seçdiyiniz istifadəçinin xəbərdarlığını silər.")
Help.add_command('mute', "<istifadəçi adı/cavablama>", "Söhbətdəki istifadəçimi susdurar, idarəçilərədə işləyir.")
Help.add_command('unmute', "<istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>", "Səssizdən çıxarar.")
Help.add_command('kick', "<istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>", "Seçdiyiniz istifadəçini qrupdan atar. (Ban etməz)")
Help.add_command('gmute', "<istifadəçi adı/cavablama> <səbəbi (istəyə bağlı)>", "İstifadəçini idarəçi olduğunuz bütün qruplarda susdurar.")
Help.add_command('ungmute', "<istifadəçi adı/cavablama>", "İstifadəçiyi qlobal olaraq səssizə alınanlar listindən silər.")
Help.add_command('gban', "<istifadəçi adı/cavablama>", "İstifadəçiyi qlobal olaraq banlayar.")
Help.add_command('ungban', "<istifadəçi adı/cavablama>", "İstifadəçiyi qlobal bandan çıxardar.")
Help.add_command('list gmute/gban', None, "Gban/Gmute olunan istifadəçilərin siyahısını əldə edin.")
Help.add_command('users', None, "Söhbətdəki bütün istifadəçiləri göstərər.")
Help.add_command('usersdel', None, "Qrup içərisində silinən hesabları göstərər.")
Help.add_command('add', "<istifadəçi adı>", "Qrupa istifadəçi əlavə edər.")
Help.add_command('pin', "<cavab>", "Cavab verdiyiniz mesajı pinləyər.")
Help.add_command('unpin','<cavab>','Sabitlənmiş mesajı sabitdən qaldırar.')
Help.add()
