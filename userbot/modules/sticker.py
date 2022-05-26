
from userbot.language import get_value
import io
import urllib.request
from PIL import Image

from telethon.tl.types import InputPeerNotifySettings
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import PAKET_ISMI, bot
from userbot.events import register
from userbot.main import PLUGIN_MESAJLAR
from telethon import events
from userbot.cmdhelp import CmdHelp

PACK_FULL = "Whoa! That's probably enough stickers for one pack, give it a break. \
A pack can't have more than 120 stickers at the moment."
PACK_DOESNT_EXIST = "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."

LANG = get_value("stickers")
LANG_ = get_value("scrapers_bot")


@register(outgoing=True, pattern="^.stik($| )?((?![0-9]).+?)? ?([0-9]*)?")
@register(outgoing=True, pattern="^.d[iı]zla($| )?((?![0-9]).+?)? ?([0-9]*)?")
async def kang(event):
    await event.edit(PLUGIN_MESAJLAR['dızcı'])
    user = await bot.get_me()
    pack_username = ''
    if not user.username:
        try:
            user.first_name.decode('ascii')
            pack_username = user.first_name
        except UnicodeDecodeError:  # User's first name isn't ASCII, use ID instead
            pack_username = user.id
    else:
        pack_username = user.username

    textx = await event.get_reply_message()
    emoji = event.pattern_match.group(2)
    # If no number specified, use 1
    number = int(event.pattern_match.group(3) or 1)
    new_pack = False
    
    if textx.photo or textx.sticker:
        message = textx
    elif event.photo or event.sticker:
        message = event
    else:
        await event.edit(LANG['GIVE_STICKER'])
        return

    sticker = io.BytesIO()
    await bot.download_media(message, sticker)
    sticker.seek(0)

    if not sticker:
        await event.edit(LANG['FAIL_DOWNLOAD'])
        return

    is_anim = message.file.mime_type == "application/x-tgsticker"
    if not is_anim:
        img = await resize_photo(sticker)
        sticker.name = "sticker.png"
        sticker.seek(0)
        img.save(sticker, "PNG")

    # The user didn't specify an emoji...
    if not emoji:
        if message.file.emoji:  # ...but the sticker has one
            emoji = message.file.emoji
        else:  # ...and the sticker doesn't have one either
            emoji = PLUGIN_MESAJLAR['emoji']

    packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
    packtitle = (f"@{user.username or user.first_name} {PAKET_ISMI} "
                 f"{number}{' animasyonlu' if is_anim else ''}")
    response = urllib.request.urlopen(
        urllib.request.Request(f'http://t.me/addstickers/{packname}'))
    htmlstr = response.read().decode("utf8").split('\n')
    new_pack = PACK_DOESNT_EXIST in htmlstr

    if new_pack:
        await event.edit(LANG['NEW_PACK'])
        await newpack(is_anim, sticker, emoji, packtitle, packname, message)
    else:
        async with bot.conversation("Stickers") as conv:
            # Cancel any pending command
            await conv.send_message('/cancel')
            await conv.get_response()

            # Send the add sticker command
            await conv.send_message('/addsticker')
            await conv.get_response()

            # Send the pack name
            await conv.send_message(packname)
            x = await conv.get_response()

            # Check if the selected pack is full
            while x.text == PACK_FULL:
                # Switch to a new pack, create one if it doesn't exist
                number += 1
                packname = f"a{user.id}_by_{pack_username}_{number}{'_anim' if is_anim else ''}"
                packtitle = (
                    f"@{user.username or user.first_name} {PAKET_ISMI} "
                    f"{number}{' animated' if is_anim else ''}")

                await event.edit(
                    LANG['TOO_STICKERS'].format(number)
                )

                await conv.send_message(packname)
                x = await conv.get_response()
                if x.text == "Invalid pack selected.":  # That pack doesn't exist
                    await newpack(is_anim, sticker, emoji, packtitle, packname)

                    # Read all unread messages
                    await bot.send_read_acknowledge("stickers")
                    # Unmute Stickers bot back
                    muted = await bot(UpdateNotifySettingsRequest(peer=429000,settings=InputPeerNotifySettings(mute_until=None)))

                    await event.edit(
                        f"💟 **Sticker {number}{'animasiyalı' if is_anim else ''} nömrəli stiker paketinə əlavə edildi.**\n"
                        f"✨ **Emoji:** {emoji}\n"
                        f"🏷 **Paket:** [{packtitle}](t.me/addstickers/{packname})",
                        parse_mode='md')
                    return

            # Upload the sticker file
            if is_anim:
                upload = await message.client.upload_file(sticker, file_name="AnimatedSticker.tgs")
                await conv.send_file(upload, force_document=True)
            else:
                sticker.seek(0)
                await conv.send_file(sticker, force_document=True)
            kontrol = await conv.get_response()

            if "Sorry, the image dimensions are invalid." in kontrol.text:
                await event.edit("`Sticker's qəbul etmədi. İkinci yol yoxlanılır...`")
                try:
                    await bot.send_file("@ezstickerbot", message, force_document=True)
                except YouBlockedUserError:
                    return await event.edit("`Zəhmət olmasa` @EzStickerBot `blokdan çıxarın və yenidən cəhd edin!`")

                try:
                    response = await conv.wait_event(events.NewMessage(incoming=True, from_users=350549033))
                    if "Please temporarily use" in response.text:
                        await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                        response = await conv.wait_event(events.NewMessage(incoming=True, from_users=891811251))

                    await bot.send_read_acknowledge(350549033)
                    await event.client.forward_messages("stickers", response.message, 350549033)
                except BaseException:
                    await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                    response = await conv.wait_event(events.NewMessage(incoming=True, from_users=891811251))
                    await bot.send_read_acknowledge(891811251)
                    await event.client.forward_messages("stickers", response.message, 891811251)

            # Send the emoji
            await conv.send_message(emoji)
            await conv.get_response()

            # Finish editing the pack
            await conv.send_message('/done')
            await conv.get_response()

    # Read all unread messages
    await bot.send_read_acknowledge(429000)
    # Unmute Stickers bot back
    muted = await bot(UpdateNotifySettingsRequest(
        peer=429000,
        settings=InputPeerNotifySettings(mute_until=None))
    )

    await event.edit(
        f"💟 **Sticker {number}{'animasiyalı' if is_anim else ''} nömrəli stiker paketinə əlavə edildi.**\n"
        f"✨ **Emoji:** {emoji}\n"
        f"🏷 **Paket:** [{packtitle}](t.me/addstickers/{packname})", parse_mode='md')


async def newpack(is_anim, sticker, emoji, packtitle, packname, message):
    async with bot.conversation("stickers") as conv:
        # Cancel any pending command
        await conv.send_message('/cancel')
        await conv.get_response()

        # Send new pack command
        if is_anim:
            await conv.send_message('/newanimated')
        else:
            await conv.send_message('/newpack')
        await conv.get_response()

        # Give the pack a name
        await conv.send_message(packtitle)
        await conv.get_response()

        # Upload sticker file
        if is_anim:
            upload = await bot.upload_file(sticker, file_name="AnimatedSticker.tgs")
            await conv.send_file(upload, force_document=True)
        else:
            sticker.seek(0)
            await conv.send_file(sticker, force_document=True)
        kontrol = await conv.get_response()
        if kontrol.message.startswith("Sorry"):
            await bot.send_file("@ezstickerbot", message, force_document=True)
            try:
                response = await conv.wait_event(events.NewMessage(incoming=True, from_users=350549033))
                if "Please temporarily use" in response.text:
                    await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                    response = await conv.wait_event(events.NewMessage(incoming=True, from_users=891811251))

                    await bot.send_read_acknowledge(350549033)
                    await bot.forward_messages("stickers", response.message, 350549033)
            except BaseException:
                await bot.send_file("@EzStickerBotBackupBot", message, force_document=True)
                response = await conv.wait_event(events.NewMessage(incoming=True, from_users=891811251))
                await bot.send_read_acknowledge(891811251)
                await bot.forward_messages("stickers", response.message, 891811251)

        # Send the emoji
        await conv.send_message(emoji)
        await conv.get_response()

        # Publish the pack
        await conv.send_message("/publish")
        if is_anim:
            await conv.get_response()
            await conv.send_message(f"<{packtitle}>")
        await conv.get_response()

        # Skip pack icon selection
        await conv.send_message("/skip")
        await conv.get_response()

        # Send packname
        await conv.send_message(packname)
        await conv.get_response()


async def resize_photo(photo):
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    scale = 512 / max(image.width, image.height)
    new_size = (int(image.width * scale), int(image.height * scale))
    image = image.resize(new_size, Image.ANTIALIAS)
    return image



@register(outgoing=True, pattern="^.q(?: |$)(.*)")
async def quotly(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit(LANG_['REPLY_TO_MSG'])
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit(LANG_['REPLY_TO_MSG'])
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit(LANG_['REPLY_TO_MSG'])
        return
    await event.edit(LANG_['QUOTING'])
    
    import telethon
    from userbot import bot
    
    await bot(telethon.tl.functions.contacts.UnblockRequest(chat))
    async with bot.conversation(chat, exclusive=False, replies_are_responses=True) as conv:
        response = None
        try:
            sayi = event.pattern_match.group(1)
            if len(sayi) == 1:
                sayi = int(sayi)
                i = 1
                mesajlar = [event.reply_to_msg_id]
                while i < sayi:
                    mesajlar.append(event.reply_to_msg_id + i)
                    i += 1
                msg = await event.client.forward_messages(chat, mesajlar, from_peer=event.chat_id)
            else:
                await reply_message.forward_to(chat)
            response = await conv.wait_event(events.NewMessage(incoming=True, from_users=1031952739), timeout=10)
        except asyncio.TimeoutError:
            await event.edit("`Botdan cavab ala bilmədim!`")
            return
        except ValueError:
            await event.edit(LANG_['QUOTLY_VALUE_ERR'])
            return

        if not response:
            await event.edit("🔸 **Botdan cavab ala bilmədim!**")
        elif response.text.startswith("Salam!"):
            await event.edit("__Məxfilik ayarlarına görə cavab ala bilmədim.__ 😒")
        else:
            await event.delete()
            await response.forward_to(event.chat_id)
        await conv.mark_read()
        await conv.cancel_all()

        
        
Help = CmdHelp('stickers')
Help.add_command('dızla', None, 'Dızla ilə bir stickerə və ya şəkili cavablayaraq öz sticker paketinizə əlavə edə bilərsiz.')
Help.add_command('q','<rəqəm>','Mətini stikerə çəvirin.')
Help.add()
